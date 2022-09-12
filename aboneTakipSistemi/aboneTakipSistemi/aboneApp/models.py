from django.db import models
from django.contrib.auth.models import User
    
class kullanimAlani(models.Model):
    kullanimAlani = models.CharField(max_length=20)
    abone_ucret = models.FloatField()
    tek_girislik_ucret = models.FloatField()
    kullanim_suresi = models.IntegerField()
    def __str__(self):
        return self.kullanimAlani

class turnikeID (models.Model):
    turnikeId = models.IntegerField(unique=True)
    turnikeAdi = models.CharField(max_length=20)
    kullanilacakAlan = models.ForeignKey(kullanimAlani,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.turnikeId)

class adminUserModel(models.Model):
    adminuser = models.OneToOneField(User, on_delete=models.CASCADE)
    telefonNumarasi = models.CharField(max_length=15)
    guncellenmeTarihi = models.DateTimeField(auto_now=True)
    hesap_olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.adminuser.username


class userInformation(models.Model):
    TYPE =(
        ("Abone","Abone"),
        ("Tek Giris","Tek Giris")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefonNumarasi = models.CharField(max_length=15)
    hesap_olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    kullanimTipi = models.CharField(max_length=20,choices=TYPE)
    bakiye = models.FloatField(default=0.0)
    kullanimAlani = models.ManyToManyField(kullanimAlani)
    admin = models.ForeignKey(adminUserModel,on_delete=models.CASCADE)
    kartId = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.user.username
        
class bakiyeLog(models.Model):
    user = models.ForeignKey(userInformation, null=True, on_delete=models.SET_NULL,related_name="bakiyelog") 
    # Kullanıcı silindiği zaman bakiye geçmişinin silinmemesini istemediğim için
    yuklenenBakiye = models.FloatField()
    yuklenenZaman = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.user.first_name

    
class aktiviteKullanimi(models.Model):
    user = models.ForeignKey(userInformation, null=True, on_delete=models.SET_NULL ,related_name="aktiviteKullanimi")
    girdigiZaman = models.DateTimeField(auto_now_add=True)
    girdigiYer = models.ForeignKey(kullanimAlani, null=True, on_delete=models.SET_NULL,related_name="aktiviteKullanimi")
    ciktigiZaman = models.DateTimeField(auto_now=True)
    giris_durumunda_mi = models.BooleanField(default=False)
    odenen_tutar = models.FloatField(default=0)
    def __str__(self):
        return self.girdigiYer

