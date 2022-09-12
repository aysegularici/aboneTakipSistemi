from serial import Serial
import sqlite3 as sql
from datetime import datetime, timedelta, timezone
import database 
import socket

class takipSistemi:
    def __init__ (self):
        self.vt = database.sorgular()
        print("-----Kart Okutun-----") 
        self.ser = Serial('COM4',9600)
        self.okuma()

    def okuma(self):
        # if self.ser.isOpen():
        #     self.ser.close()
        # self.ser.open()
        UDP_IP = "169.254.119.36"
        UDP_PORT = 8888
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.bind((UDP_IP, UDP_PORT))
        
        while True:
            self.hexData,addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            # self.hexDataa = self.ser.readline().strip()
            # print("received message: ",addr)
            # print("-----Kart Okutun-----")
            if(len(self.hexData)>0):
                self.hexData = str(self.hexData)
                self.kartIdBulma()

    def kullanicigetir(self):
        liste = self.vt.sartSelect(sart_adi='kartId',istenen_id=self.kart_id)
        print(liste)
        if len(liste)>0:
            user_id = str(liste).split(',')
            user_id = user_id[0]
            self.user_id = str(user_id).strip('[(')
            self.alanYetkileriBulma()
        else:
            print("-----Kullanıcı Kayıtlı Değil-----\n")
       
    def kartIdBulma(self):
        x = self.hexData.find("UID:")
        if(x>0):
            self.kart_id = self.hexData[(x+4):-1:]
            self.kart_id = str(self.kart_id)
            print(self.kart_id)
            self.kullanicigetir()
        # else:
        #     print("-----Kart Okutun-----")

    def alanYetkileriBulma(self):
        alan_yetkileri = self.vt.sartSelect('kullanimalani_id','aboneApp_userInformation_kullanimAlani', 'userinformation_id',self.user_id)
        alan = list() # Alanın içerisinde User id ye göre kullanım alanı yetkileri
        for i in alan_yetkileri:
            alan.append(i[0]) # Fazla Karakterlerden Temizlenmesi için 
        self.turnikeId = list()
        for i in alan:
            turnike = self.vt.sartSelect('turnikeId','aboneApp_turnikeid', 'kullanilacakAlan_id',i)
            for j in turnike:
                self.turnikeId.append(j[0])
        # Turnikeid nin içerisinde Alan yetkilerine göre girebileceği Turnike numaraları var
        print("Kullanıcının Yetkisi Olduğu Turnike Numaraları: ",self.turnikeId)
        print("Kullanıcının Yetkisi Olduğu Alanlar: ",alan)
        self.girisTurnikeNo()

    def girisTurnikeNo(self):
        z = self.hexData.find("TNO:")
        turnike_no = self.hexData[z+4] 
        self.turnike_no = str(turnike_no)
        print("Turnike Numarası:",self.turnike_no)
        # turnike_no nun içerisinde Şuan giriş yapmak istediği turnike numarası var
        girdigi_alan = self.vt.sartSelect('kullanilacakAlan_id','aboneApp_turnikeid', 'turnikeId',self.turnike_no)
        girdigi_yer_id = str(girdigi_alan).split(',')
        girdigi_yer_id = girdigi_yer_id[0]
        self.girdigi_yer_id = girdigi_yer_id.strip('[(')
        temp = 1
        for i in self.turnikeId:
            if (self.turnike_no == str(i)):
                temp = 0
                print("Kullanım Alanı İd:",self.girdigi_yer_id)
                self.kullaniciGiris()
        if(temp):
            # Bu Turnike numarası Bir Alana Kayıtlı mı
            alan_var_mi = self.vt.select_sorgusu(getir='kullanilacakAlan_id',tablo_adi='aboneApp_turnikeID')
            turnike_alan = list()
            temp2 = 0
            for i in alan_var_mi:
                turnike_alan.append(i[0])
            for i in turnike_alan:
                if (self.turnike_no == str(i)):
                    temp2 = 1
            
            if(temp2):
                print("-----Giriş Yetkiniz Yok-----\n")
            else:
                print("-----Turnike Numarası Kayıtlı Değil-----\n")

    def kullaniciGiris(self):
        # Kullanıcının boolean değer olan giris_durumunda_mi değişkeni kontrol ediliyor. Eğer 1 ise çıkışa yönlendirilecek 0 ise giris islemleri gerçekleşecek.
        giris_durumu = self.vt.sartSelect('giris_durumunda_mi','aboneApp_aktiviteKullanimi','user_id',self.user_id)


        bakiye = self.vt.sartSelect('bakiye','aboneApp_userInformation','id',self.user_id)
        bakiye = bakiye[0]
        bakiye = str(bakiye).strip('(,)')
        self.bakiye = float(bakiye)

        self.kullanim_tipi = self.vt.sartSelect(getir='kullanimTipi',istenen_id=self.user_id)    
        ucret = self.vt.ucGetirSelect(istenen_id=self.girdigi_yer_id)
        ucret = str(ucret).strip('[]()')
        ucret = str(ucret).split(',')
        abone = float(ucret[0])
        tek = float(ucret[1])
        kullanim_suresi = float(ucret[2])
        print("Kullanım Süresi: ",kullanim_suresi)

        temp = 1
        for i in giris_durumu:
            if(i[0]==1):
                temp = 0
                self.kullaniciCikis()

        if temp:  
            if (self.kullanim_tipi[0]==('Abone',)):
                tutar = kullanim_suresi * abone
            else: 
                tutar = kullanim_suresi * tek
            tutar = float(tutar)
            if self.bakiye<tutar:
                print("-----Bakye yetersiz-----\n")
                self.okuma()
            print("-----Kullanıcı Girişi-----\n")
            self.vt.insertinto(deger1=datetime.now(),deger2=self.girdigi_yer_id, deger3=self.user_id,deger4=datetime.now())
            temp = 0
                

    def kullaniciCikis(self):

        # girdigi_alan = self.vt.sartSelect('kullanilacakAlan_id','aboneApp_turnikeid', 'turnikeId',self.turnike_no)
        # girdigi_yer_id = str(girdigi_alan).split(',')
        # girdigi_yer_id = girdigi_yer_id[0]
        # self.girdigi_yer_id = girdigi_yer_id.strip('[(')

        # ucret = self.vt.ucGetirSelect(istenen_id=self.girdigi_yer_id)
        # ucret = str(ucret).strip('[]()')
        # ucret = str(ucret).split(',')
        # self.abone = float(ucret[0])
        # self.tek = float(ucret[1])
        # self.kullanim_suresi = float(ucret[2])
        # print("Kullanım Süresi: ",self.kullanim_suresi)

        # temp = 1
        # for i in giris_durumu:
        #     if(i[0]==1):
        #         temp = 0
                


        girdigi_alan = self.vt.ikiSartSelect("girdigiYer_id","aboneApp_aktiviteKullanimi","giris_durumunda_mi",1,"user_id",self.user_id)
        # girdigi_alan = self.vt.sartSelect('kullanilacakAlan_id','aboneApp_turnikeid', 'turnikeId',self.turnike_no)
        girdigi_yer = str(girdigi_alan).split(',')
        girdigi_yer = girdigi_yer[0]
        girdigi_yer = girdigi_yer.strip('[(')


        print("Çıkış Yapılacak Alan İd:",girdigi_yer)

        
        ucret = self.vt.ucGetirSelect(istenen_id=girdigi_yer)
        ucret = str(ucret).strip('[]()')
        ucret = str(ucret).split(',')
        abone = float(ucret[0])
        tek = float(ucret[1])
        kullanim_suresi = float(ucret[2])
        print("Kullanım Süresi: ",kullanim_suresi)



        girdigi_zaman = self.vt.ikiSartSelect(istenen_id=self.user_id)
        girdigi_zaman = str(girdigi_zaman).strip("'(),[]")
        x = girdigi_zaman.find('.')
        girdigi_zaman = girdigi_zaman[:x:]
        girilen_zaman = datetime.strptime(girdigi_zaman,'%Y-%m-%d %H:%M:%S')
        ciktigi_zaman = datetime.now()
        diff = ciktigi_zaman - girilen_zaman
        diff.total_seconds()
        diff = int(diff/ timedelta(minutes=1)) # İçeride geçirilen dakika cinsinden süre
        print("İçeride kalınan süre: ",diff)
        print("Kullanım Süresi: ",kullanim_suresi)
        if (self.kullanim_tipi[0]==('Abone',)):
            if(kullanim_suresi < diff):
                tutar = diff * abone
            else:
                tutar = kullanim_suresi * abone
            print("Abone Dakika Ücreti: ",abone)
        else:
            if(kullanim_suresi < diff):
                tutar = diff * tek
            else:
                tutar = kullanim_suresi * tek
            print("Tek Kullanım Dakika Ücreti: ",tek)
        print("Tutar: ",tutar)
        print("bakiye",self.bakiye)

        self.bakiye = self.bakiye - tutar
        print("BAKİYE",self.bakiye)        
        print("-----Kullanıcı Çıkışı-----")
        self.vt.update(yeni_deger=self.bakiye,istenen_id=self.user_id)
        self.vt.update2(yeni_deger2= tutar,istenen_id= self.user_id)

if __name__ =='__main__':
    tp = takipSistemi()      



