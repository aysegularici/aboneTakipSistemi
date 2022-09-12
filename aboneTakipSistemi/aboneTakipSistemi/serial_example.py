from serial import Serial
import sqlite3 as sql

class takipSistemi:
    def __init__ (self,kartId,userId,turnikeId,state):
        self.kartId = kartId
        self.userId = userId
        self.turnikeId = turnikeId
        self.state = state

def yol():
    db = sql.connect("C:/Users/Casper/Desktop/DjangoProjelerim/aboneTakipSistemi/aboneTakipSistemi/db.sqlite3")
    return(db.cursor())
def okuma():
    while True:
        hexData = ser.readline().strip()
        if(len(hexData)>0):
            ayiklama(hexData)
def kullanicigetir(kart_id):
    imlec = yol()
    imlec.execute("select * from aboneApp_userinformation where kartId = '{}'".format(kart_id))
    liste = imlec.fetchall()
    if liste>0:
        return(liste)
    else:
        print("Kullanıcı Kayıtlı Değil")
def kartIdBulma(hexData):
    x = str(hexData).find("UID:")
    if(x>0):
        komut_list = str(hexData)
        kart_id = komut_list[(x+4):-1:]
        return(kart_id)
    else:
        print("Kart Okutun")
        okuma()
def userIdBulma(liste):
    user_id = str(liste).split(',')
    user_id = user_id[0]
    user_id = str(user_id).strip('[(')
def alanYetkileriBulma(user_id):
    imlec = yol()
    imlec.execute("select kullanimalani_id from aboneApp_userInformation_kullanimAlani where userinformation_id = '{}'".format(user_id))
    alan_yetkileri = imlec.fetchall()
    alan = list()
    for i in alan_yetkileri:
        alan.append(i[0]) # Fazla Karakterlerden Temizlenmesi için 
    turnikeId = list()
    for i in alan:
        imlec.execute("select turnikeId from aboneApp_kullanimAlani where id = '{}'".format(i))
        turnike = imlec.fetchall()
        for j in turnike:
            turnikeId.append(j[0])
    return(turnikeId)
def girisTurnikeNo(hexData,turnike_yetkileri):
    imlec = yol()
    z = str(hexData).find("TNO:")
    turnike_no = str(hexData)[z+4] 
    imlec.execute("select * from aboneApp_kullanimAlani where turnikeId = '{}'".format(turnike_no))      
    girdigi_alan = imlec.fetchall()
    if(len(girdigi_alan==0)):
        print("Kullanım Alanı Kayıtlı Değil")
        return
    alan=list()
    if turnike_no in turnike_yetkileri:
        print("Giriş Yapıldı")


def ayiklama(hexData):
    kart_id = kartIdBulma(hexData)
    liste = kullanicigetir(kart_id)
    user_id = userIdBulma(liste)
    turnike_yetkileri = alanYetkileriBulma(user_id)
    girisTurnikeNo(hexData,turnike_yetkileri)

if __name__ =='__main__':
    ser = Serial('COM8',9600)
    if ser.isOpen():
        ser.close()
    ser.open()
    okuma()


# ser = Serial('COM8',9600)
# if ser.isOpen():
#     ser.close()
# ser.open()
# db = sql.connect("C:/Users/Casper/Desktop/DjangoProjelerim/aboneTakipSistemi/aboneTakipSistemi/db.sqlite3")
# imlec = db.cursor()
# while True:
#     hexData = ser.readline().strip()
#     print(hexData)
#     x = str(hexData).find("UID:")
#     #print(x)
#     if(x>0):
#         komut_list = str(hexData)
#         kart_id = komut_list[(x+4):-1:]
#         print(str(kart_id))
#         imlec.execute("select * from aboneApp_userinformation where kartId = '{}'".format(kart_id))
#         liste = imlec.fetchall()

#         if len(liste) > 0 :
#             print(liste)
#             user_id = str(liste).split(',')
#             user_id = user_id[0]
#             user_id = str(user_id).strip('[(')
#             print(user_id)
#             imlec.execute("select kullanimalani_id from aboneApp_userInformation_kullanimAlani where userinformation_id = '{}'".format(user_id))
#             alan_yetkileri = imlec.fetchall()
#             alan=[]
#             for i in alan_yetkileri:
#                 alan.append(i[0])
#             print(alan)
#             z = str(hexData).find("TNO:")
#             #print(z)
#             alan_no = komut_list[z+4] 
#             print(alan_no)
#             imlec.execute("select * from aboneApp_kullanimAlani where turnikeId = '{}'".format(alan_no))
#             girdigi_alan = imlec.fetchall()
#             if len(girdigi_alan)==0:
#                 print("Kullanım Alanı Kayıtlı Değil")
#             else:
#                 print(alan_no)
#                 print(girdigi_alan)
#                 if(int(alan_no) in alan):
                    
#                     print("Giriş Yapıldı")
#                 else:
#                     print("Alan yetkisi yok")
#         else:
#             print("Kullanıcı Kayıtlı Değil")

