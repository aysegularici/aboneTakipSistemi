from pickle import FALSE
import sqlite3 as sql

class sorgular:
    def __init__(self):
        self.yol = "db.sqlite3"
        self.baglan()
    def baglan(self):
        self.db = sql.connect(self.yol)
        self.cursor = self.db.cursor()

    def select_sorgusu(self,getir="*",tablo_adi="aboneApp_userInformation"):
        self.cursor.execute("select {} from {} ".format(getir,tablo_adi))
        liste = self.cursor.fetchall()
        return liste
    def sartSelect(self,getir="*",tablo_adi="aboneApp_userInformation",sart_adi="id",istenen_id=1):
        self.cursor.execute("select {} from {} where {} = '{}'".format(getir,tablo_adi,sart_adi,istenen_id))
        liste = self.cursor.fetchall()
        return liste
    def ikiSartSelect(self,getir="girdigiZaman",tablo_adi="aboneApp_aktiviteKullanimi",sart_adi="user_id",istenen_id=1,sart_adi2='giris_durumunda_mi',ikinci_istenen = 1):
        self.cursor.execute("select {} from {} where {} = '{}' and {} = '{}'".format(getir,tablo_adi,sart_adi,istenen_id,sart_adi2,ikinci_istenen))
        liste = self.cursor.fetchall()
        return liste

     
    def ucGetirSelect(self,getir="abone_ucret",getir2='tek_girislik_ucret',getir3='kullanim_suresi',tablo_adi="aboneApp_kullanimalani",sart_adi="id",istenen_id=1):
        self.cursor.execute("select {},{},{} from {} where {} = '{}'".format(getir,getir2,getir3,tablo_adi,sart_adi,istenen_id))
        liste = self.cursor.fetchall()
        return liste
    def update(self,tablo_adi='aboneApp_userInformation',degisecek = 'bakiye',yeni_deger = 1,sart_adi = 'id',istenen_id = 1):
        # sql_update1 = """UPDATE ? SET ? = ? WHERE ? = ?"""
        # veri = (tablo_adi,degisecek,yeni_deger,sart_adi,istenen_id)
        self.cursor.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(tablo_adi,degisecek,yeni_deger,sart_adi,istenen_id))
        self.db.commit()
    def update2(self,tablo_adi='aboneApp_aktiviteKullanimi',degisecek = 'giris_durumunda_mi',yeni_deger = 0,degisecek2='odenen_tutar',yeni_deger2=1,sart_adi = 'user_id', istenen_id = 1,sart_adi2 = 'giris_durumunda_mi',istenen_id2 = 1):
        # print("UPDATE {} SET {} = '{}', {} ='{}' WHERE {} = '{}' AND {}= '{}'".format(tablo_adi,degisecek,yeni_deger,degisecek2,yeni_deger2,sart_adi,istenen_id,sart_adi2,istenen_id2))
        self.cursor.execute("UPDATE {} SET {} = '{}', {} ='{}' WHERE {} = '{}' AND {}= '{}'".format(tablo_adi,degisecek,yeni_deger,degisecek2,yeni_deger2,sart_adi,istenen_id,sart_adi2,istenen_id2))
        self.db.commit()
    def insertinto(self,tablo_adi='aboneApp_aktiviteKullanimi',column1='girdigiZaman',column2='girdigiYer_id',column3='user_id',column4='ciktigiZaman',column5='giris_durumunda_mi',column6='odenen_tutar',deger1=1,deger2=1,deger3=1,deger4=1,deger5=1,deger6=0):
        self.cursor.execute("INSERT INTO {} ({},{},{},{},{},{}) VALUES ('{}','{}','{}','{}','{}','{}')".format(tablo_adi,column1,column2,column3,column4,column5,column6,deger1,deger2,deger3,deger4,deger5,deger6))
        self.db.commit()
