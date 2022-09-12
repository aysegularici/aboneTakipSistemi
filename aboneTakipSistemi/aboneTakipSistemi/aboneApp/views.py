from asyncio.windows_events import NULL
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date
from datetime import timedelta
# import pagination
from django.core.paginator import Paginator

def login_view(request):
    if request.method=='POST':
        username = request.POST['ad']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                return redirect('aboneApp:dashboard')
                #Anasayfa tasarımı yapıldığında bu kısıma eklenecek
            else:
                messages.info(request, 'Admin Harici Giremez')
                return redirect('aboneApp:login')
        else:
            messages.info(request,'Geçersiz Kimlik')
            return redirect('aboneApp:login')
    else:
        return render(request,'login.html')

def kullanici_listeleme(request):
    if request.user.is_authenticated and request.user.is_superuser:
        kullanicilar=userInformation.objects.all()
        context={

            'kullanicilar' : kullanicilar,
        }
        return render(request, 'tableUser.html', context)
    return redirect('aboneApp:login')

def kullanici_arama(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        arama = get_object_or_404(userInformation, id=id)
        data_kullanim = arama.kullanimAlani.all()
        kullanici_gecmis = aktiviteKullanimi.objects.filter(user__id = arama.id)
        gecmis = kullanici_gecmis.order_by()[::-1]
        # p = Paginator(gecmis.objects.all(), 3)
        # page = request.GET.get('page')
        # gecmis_list = p.get_page(page)

        bakiye = bakiyeLog.objects.filter(user__id = arama.id)
        bakiye = bakiye.order_by()[::-1]
        context = {
            'arama' : arama,
            'data':data_kullanim,
            'gecmis' : gecmis,
            # 'gecmis_list':gecmis_list,
            'bakiye':bakiye,
        }
        return render(request, 'arama.html', context)
    return redirect('aboneApp:login')

def rapor(request):
    if request.user.is_authenticated and request.user.is_superuser:
        today = date.today()
        rapor = userInformation.objects.filter(hesap_olusturma_tarihi__year =today.year,hesap_olusturma_tarihi__month =today.month,hesap_olusturma_tarihi__day =today.day)  
        context = {
            'rapor' : rapor,
        }
        return render(request, 'rapor.html',context)
    return redirect('aboneApp:login')

def aylik_rapor(request):
    if request.user.is_authenticated and request.user.is_superuser:
        today = date.today()
        rapor = userInformation.objects.filter(hesap_olusturma_tarihi__year =today.year,hesap_olusturma_tarihi__month =today.month)
        context = {
            'rapor' : rapor,
        }
        return render(request, 'aylikRapor.html',context)
    return redirect('aboneApp:login')

def logout(request):
	auth.logout(request)
	return redirect('aboneApp:login') 

def ayarlar(request,id): # güncelleme için ayarlar html'line seçilen satrın id siyle
    if request.user.is_authenticated  and request.user.is_superuser: 
        guncelle = userInformation.objects.get(id=id)
        alan=kullanimAlani.objects.all()
        return render(request,'ayarlar.html', {'guncelle':guncelle},{'alan': alan})
    return redirect('aboneApp:login')
    
def guncelleFonksiyon(request,id):
    if request.user.is_authenticated  and request.user.is_superuser:
        guncelle = userInformation.objects.get(id=id)
        alan=kullanimAlani.objects.all()
        context={

            'alan' : alan,
            'guncelle': guncelle,
        }
        if request.method == 'POST':
            ad = request.POST['ad']
            soyad = request.POST['soyad']
            yeni_telefon=request.POST['telefon']
            yeni_kullanimTipi = request.POST['kullanimTipi']
            yeni_kullanimAlani = request.POST.getlist('kullanimAlani')
            yeni_kart =request.POST['kartId']
            e_mail = request.POST['email']
            kontrol = userInformation.objects.all()
            for i in kontrol:
                if (yeni_telefon == i.telefonNumarasi):
                    if(yeni_telefon==guncelle.telefonNumarasi):
                        continue
                    messages.success(request,'Telefon Numarasi Baska bir kullanicida kayitli.!')
                    print("Telefon Numarasi kayitli.!")
                    return render(request,'ayarlar.html', context)
                elif (e_mail == i.user.email):
                    if(e_mail==guncelle.user.email):
                        continue
                    messages.success(request,'Email baska bir kullanicida kayitli.!')
                    return render(request,'ayarlar.html', context)
                elif(yeni_kart == i.kartId):
                    if(yeni_kart==guncelle.kartId):
                        continue
                    messages.success(request,'Kart Başka Bir Kullanıcıda Kayıtlı.!')
                    return render(request,"ayarlar.html")
            user_ =userInformation.objects.get(id=id)
            User.objects.filter(id=user_.user.id ).update(first_name = ad,last_name=soyad,email=e_mail)
            kayit = userInformation.objects.filter(id=id).update(kullanimTipi = yeni_kullanimTipi, telefonNumarasi=yeni_telefon, kartId=yeni_kart)
            aa = userInformation.objects.get(id = id)
            if len(yeni_kullanimAlani)>0:
                aa.kullanimAlani.clear()
                for i in yeni_kullanimAlani:
                    print(type(i),i)
                    aa.kullanimAlani.add(kullanimAlani.objects.get(id = int(i)))
            messages.success(request,'Guncelleme Başarılı')
            return redirect('aboneApp:kullanici_listeleme')
        else:
            return render(request,'ayarlar.html', context)
    return redirect('aboneApp:login')    

def sil(request,id):
    if request.user.is_authenticated  and request.user.is_superuser:
        if aktiviteKullanimi.objects.filter(user__id = id ,  giris_durumunda_mi = True).exists():# GİRİLİ OLAN KULLANICI SİLİNMEMESİ İÇİN
                messages.warning(request,"KULLANICI ÇIKIŞ YAPMAMIŞ")
                return redirect("aboneApp:kullanici_listeleme")
        aboneBilgisi=get_object_or_404(userInformation, id=id)
        aboneBilgisi.kullanimAlani.clear()
        # x = User.objects.get(id=aboneBilgisi.user.id)
        # ad = x.first_name
        # if ((ad[0]=='(') and (ad[8]==')')):
        #     pass
        # else:    
        #     ad = '(Silindi)'+ str(ad)
        #     User.objects.filter(id=x.id ).update(first_name = ad)
        
        # nul = NULL
        # kayit = userInformation.objects.filter(id=id).update(kullanimTipi = nul, bakiye = 0, kartId = nul)
        aboneBilgisi.delete()
        return redirect('aboneApp:kullanici_listeleme') 
    return redirect('aboneApp:login')  

def kullanimAlanisil(request,id):
    if request.user.is_authenticated  and request.user.is_superuser:
        aboneBilgisi=get_object_or_404(kullanimAlani, id=id)
        aboneBilgisi.delete()
        return redirect('aboneApp:kullanimAlaniListeleme') 
    return redirect('aboneApp:login')  

def kullaniciEkle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        alan=kullanimAlani.objects.all()
        context={

            'alan' : alan,
        }
        if request.method == 'POST':
            ad = request.POST['ad']
            soyad = request.POST['soyad']
            e_mail = request.POST['email']
            yeni_telefon=request.POST['telefon']
            yeni_bakiye=request.POST['bakiye']
            yeni_kullanimTipi = request.POST['kullanimTipi']
            kullanimAlani_2=request.POST.getlist('kullanimAlani')
            yeni_username = request.POST['username']
            yeni_kart =request.POST['kartId']
            adminuser = adminUserModel.objects.get(id=1)
            kontrol = userInformation.objects.all()
            for i in kontrol:
                if (yeni_telefon == i.telefonNumarasi):
                    messages.success(request,'Telefon Numarası Başka Bir Kullanıcıda Kayıtlı.!')
                    return render(request,"kullaniciEkle.html")
                elif (e_mail == i.user.email):
                    messages.success(request,'Email Başka Bir Kullanıcıda Kayıtlı.!')
                    return render(request,"kullaniciEkle.html")
                elif (yeni_username == i.user.username):
                    messages.success(request,'Kullanıcı Adı Başka Bir Kullanıcıda Kayıtlı.!')
                    return render(request,"kullaniciEkle.html")
                elif(yeni_kart == i.kartId):
                    messages.success(request,'Kart Başka Bir Kullanıcıda Kayıtlı.!')
                    return render(request,"kullaniciEkle.html")

            user2 = User.objects.create(username = yeni_username, first_name = ad, last_name = soyad, email = e_mail)
            kayit = userInformation.objects.create(admin = adminuser, user=user2,kullanimTipi = yeni_kullanimTipi, telefonNumarasi=yeni_telefon, bakiye=yeni_bakiye, kartId=yeni_kart)
            bakiye_kayit = bakiyeLog.objects.create(user = kayit , yuklenenBakiye = yeni_bakiye) 
            for i in kullanimAlani_2:
                kayit.kullanimAlani.add(i)
                kayit.save()
            messages.success(request,'Ekleme Başarılı')
            return redirect('aboneApp:kullanici_listeleme')
        return render(request,"kullaniciEkle.html",context)
    return redirect('aboneApp:login')

def kullanimAlaniListeleme(request):
    if request.user.is_authenticated and request.user.is_superuser:
        alan=kullanimAlani.objects.all()
        turnike = turnikeID.objects.all()
        liste = list()
        for j in alan:
            for i in turnike:
                if(i.kullanilacakAlan.id == j.id):
                    print(j.kullanimAlani,i.turnikeId)
        context={

            'alan' : alan,
            'turnike': turnike,
        }
        return render(request, 'kullanimAlaniListeleme.html', context)
    return redirect('aboneApp:login')

def kullanimAlaniEkle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            ad=request.POST['ad']
            abone_ucret=request.POST['abone_ucret']
            tek_girislik_ucret=request.POST['tek_girislik_ucret']
            kullanim_suresi=request.POST['kullanim_suresi']
            kontrol = kullanimAlani.objects.all()
            for i in kontrol:
                if (ad == i.kullanimAlani):
                    messages.success(request,'Kullanım Alanı kayıtlı')
                    return render(request,"kullanimAlaniEkle.html")
            kayit = kullanimAlani.objects.create(kullanimAlani=ad,abone_ucret = abone_ucret, tek_girislik_ucret=tek_girislik_ucret, kullanim_suresi=kullanim_suresi)
            messages.success(request,'Ekleme Başarılı')
            return redirect('aboneApp:kullanimAlaniListeleme')
        return render(request,"kullanimAlaniEkle.html")
    return redirect('aboneApp:logout')

def kullanimAlaniGuncellemeAyari(request,id):
    if request.user.is_authenticated  and request.user.is_superuser: 
        guncelle = kullanimAlani.objects.get(id=id)
        return render(request,'kullanimAlaniGuncelle.html', {'guncelle':guncelle})
    return redirect('aboneApp:login')

def kullanimAlaniGuncelle(request,id):
    if request.user.is_authenticated  and request.user.is_superuser: 
        guncelle = kullanimAlani.objects.get(id=id)
        if request.method == 'POST':
            ad=request.POST['ad']
            yeni_abone_ucret=request.POST['abone_ucret']
            yeni_tek_girislik_ucret=request.POST['tek_girislik_ucret']
            yeni_kullanim_suresi=request.POST['kullanim_suresi']
            turnike_numarasi=request.POST['turnikeId']
            kontrol = kullanimAlani.objects.all()
            for i in kontrol:
                if (ad == i.kullanimAlani):
                    if (ad == guncelle.kullanimAlani):
                        continue
                    messages.success(request,'Kullanım Alanı Kayıtlı')
                    print("Kullanım Alanı kayıtlı")
                    return render(request,'kullanimAlaniGuncelle.html', {'guncelle':guncelle})
            kullanimAlani.objects.filter(id=id).update(trnikeId=turnike_numarasi, kullanimAlani = ad, abone_ucret = yeni_abone_ucret, tek_girislik_ucret = yeni_tek_girislik_ucret, kullanim_suresi=yeni_kullanim_suresi)
            messages.success(request,'Güncelleme Başarılı')
            return redirect('aboneApp:kullanimAlaniListeleme')
        return render(request,'kullanimAlaniGuncelle.html', {'guncelle':guncelle})
    return redirect('aboneApp:login')

def turnikeEkle(request):
    if request.user.is_authenticated  and request.user.is_superuser: 
        alan=kullanimAlani.objects.all()
        turniketablo = turnikeID.objects.all()
        turnike_list = ["1","2","3","4","5","6","7"]
        for turnik in turniketablo:
            if str(turnik.turnikeId) in turnike_list:
                turnike_list.remove(str(turnik.turnikeId)) 
        print(turnike_list)
        context={

            'alan' : alan,
            'liste': turnike_list,
        }
        if request.method == 'POST':
            k_alan = request.POST['kullanimAlani']
            turnike_numaralari = request.POST.getlist('turnikeId')
            k_alan = kullanimAlani.objects.get(id = k_alan)
            for i in turnike_numaralari:
                turnikeID.objects.create(turnikeId =i,kullanilacakAlan = k_alan, turnikeAdi = k_alan.kullanimAlani+'-'+i)  
            messages.success(request,'Ekleme Başarılı')
            return redirect('aboneApp:kullanimAlaniListeleme')
        return render(request,'turnikeEkle.html', context)
    return render(request,'login.html')

def turnike_guncelle(request,id):
    if request.user.is_authenticated  and request.user.is_superuser: 
        guncelle = kullanimAlani.objects.get(id=id)
        temp = turnikeID.objects.filter(kullanilacakAlan=guncelle)
        print(temp)
        temp.delete()
        alan=kullanimAlani.objects.all()
        turniketablo = turnikeID.objects.all()
        turnike_list = ["1","2","3","4","5","6","7"]
        for turnik in turniketablo:
            if str(turnik.turnikeId) in turnike_list:
                turnike_list.remove(str(turnik.turnikeId)) 
        print(turnike_list)
        context={

            'alan' : alan,
            'liste': turnike_list,
            'guncelle':guncelle,
        }
        if request.method == 'POST':
            # k_alan = request.POST['kullanimAlani']
            turnike_numaralari = request.POST.getlist('turnikeId')
            # k_alan = kullanimAlani.objects.get(id = k_alan)
            for i in turnike_numaralari:
                turnikeID.objects.create(turnikeId =i,kullanilacakAlan = guncelle, turnikeAdi = guncelle.kullanimAlani+'-'+i)  
            messages.success(request,'Guncelleme Başarılı')
            return redirect('aboneApp:kullanimAlaniListeleme')  
        return render(request,'turnikeGuncelle.html',context)
    return render(request,'login.html', context) 

def bakiye_yukleme_ayarlari(request,id):
    if request.user.is_authenticated  and request.user.is_superuser: 
        guncelle = userInformation.objects.get(id=id)
        return render(request,'bakiyeYukleme.html', {'guncelle':guncelle})
    return redirect('aboneApp:login')

def bakiye_yukle(request,id):
    if request.user.is_authenticated  and request.user.is_superuser:
        # guncelle = userInformation.objects.get(id=id)
        guncelle = get_object_or_404(userInformation, id=id)
        alan = guncelle.kullanimAlani.all()
        context={
            'guncelle': guncelle,
        }
        if (len(alan)<1): #KULLANIM ALANI YETKİSİ YOKKEN BAKİYE YÜKLENMEMESİ İÇİN
            messages.warning(request,"KULLANIM ALANI YETKİSİ YOK")
            return redirect('aboneApp:kullanici_listeleme')
        if request.method == 'POST':
            yeni_bakiye = request.POST['bakiye']
            float(yeni_bakiye)
            user_ = User.objects.filter(id=guncelle.user.id )
            bakiyeLog.objects.create(user = guncelle , yuklenenBakiye = yeni_bakiye)            
            eski_bakiye = guncelle.bakiye
            yeni_bakiye = float(yeni_bakiye) + float(eski_bakiye)
            kayit = userInformation.objects.filter(id=id).update(bakiye = yeni_bakiye)
            messages.warning(request,"Bakiye Yüklendi")
            return redirect('aboneApp:dashboard')
        return render(request,'bakiyeYukleme.html', context)
    return redirect('aboneApp:login')
    
def kullanici_giris(request,id):
    if request.user.is_authenticated  and request.user.is_superuser: 
        giris = get_object_or_404(userInformation, id=id)
        alan = giris.kullanimAlani.all() # Giriş yetkilendirme için 
        if (len(alan)<1): #KULLANIM ALANI YETKİSİ YOKKEN GİRİŞ EKRANINA GEÇEMEMESİ İÇİN
            messages.warning(request,"KULLANIM ALANI YETKİSİ YOK")
            return redirect('aboneApp:kullanici_listeleme')
        
        context={
            'alan' : alan,
            'giris': giris,
        }
        if aktiviteKullanimi.objects.filter(user__id = id ,  giris_durumunda_mi = True).exists():
                messages.warning(request,"KULLANICI ZATEN İÇERİDE")
                return redirect("aboneApp:kullanici_listeleme")
        if request.method == 'POST':
            kullanacagi_alan = request.POST['kullanimAlani']
            girdigiYer = kullanimAlani.objects.get(id=int(kullanacagi_alan))
            user2 = giris.kullanimTipi
            k_sure = girdigiYer.kullanim_suresi
            if( giris.bakiye<(girdigiYer.abone_ucret*girdigiYer.kullanim_suresi)):
                messages.warning(request,"Kullanım Alanı İçin Bakiye Yetersiz.. ")
                return redirect('aboneApp:kullanici_listeleme')
            kayit = aktiviteKullanimi.objects.create(user = giris, girdigiYer = girdigiYer, giris_durumunda_mi = True)
            messages.warning(request,"KULLANICI GİRİŞİ")
            return redirect('aboneApp:dashboard')
        return render(request,'kullanici_giris.html', context)
    return redirect('aboneApp:login')

def kullanici_cikis(request,id):
    if request.user.is_authenticated  and request.user.is_superuser: 
        cikis_id = get_object_or_404(userInformation, id=id)
        if aktiviteKullanimi.objects.filter(user__id = id ,  giris_durumunda_mi = True).exists():
            data = aktiviteKullanimi.objects.filter(user__id = id , giris_durumunda_mi=True)
            for data in data:
                giris = data.girdigiZaman
                cikis = timezone.now()
                alan = data.girdigiYer
                diff = cikis-giris
            diff.total_seconds()
            diff = int(diff / timedelta(minutes=1))
            k_alan = kullanimAlani.objects.get(kullanimAlani=alan)
            user2 = cikis_id.kullanimTipi
            k_sure = k_alan.kullanim_suresi
            if (diff>k_sure and user2=='TekKullanim'):
                tutar =(k_alan.tek_girislik_ucret)*diff
            elif(diff>k_sure and user2=='Abone'):
                tutar = (k_alan.abone_ucret)*diff
            elif(diff<=k_sure and user2=='TekKullanim'):
                tutar = (k_alan.tek_girislik_ucret)*k_sure
            elif(diff<=k_sure and user2=='Abone'):
                tutar = (k_alan.abone_ucret)*k_sure
            
            eski_bakiye = cikis_id.bakiye
            yeni_bakiye = float(eski_bakiye) - tutar
            kayit = userInformation.objects.filter(id=id).update(bakiye=yeni_bakiye)
            aktiviteKullanimi.objects.filter(user__id = id, giris_durumunda_mi=True).update(giris_durumunda_mi=False,ciktigiZaman = timezone.now(), odenen_tutar = tutar)
            mesaj = "Kullanıcı Çıkışı.!  Tutar:{}".format(tutar)
            messages.warning(request,mesaj)
            return redirect('aboneApp:dashboard') 
        messages.warning(request,"KULLANICI GİRİŞ YAPMAMIŞ")
        return redirect("aboneApp:kullanici_listeleme")
    return redirect('aboneApp:login')

def bakiye_raporu(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        bakiye = bakiyeLog.objects.all()
        bakiye = bakiye.order_by()[::-1]
        context={

            'bakiye' : bakiye,
        }
        return render(request, 'bakiye_rapor.html', context)

    return redirect('aboneApp:login') 

def dashboard(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bugun_giris = aktiviteKullanimi.objects.filter(girdigiZaman__year =today.year,girdigiZaman__month =today.month,girdigiZaman__day =today.day)
        kullanicilar = userInformation.objects.all()
        suan_icerde_sayisi=0
        suan_icerde = aktiviteKullanimi.objects.filter(giris_durumunda_mi = True)

        ay_giris = aktiviteKullanimi.objects.filter(girdigiZaman__year =today.year,girdigiZaman__month =today.month) 
        bugun_bakiye = bakiyeLog.objects.filter(yuklenenZaman__year =today.year,yuklenenZaman__month =today.month,yuklenenZaman__day =today.day)
        ay_bakiye = bakiyeLog.objects.filter(yuklenenZaman__year =today.year,yuklenenZaman__month =today.month)
        bugun_giris_sayisi = len(bugun_giris)   
        suan_icerde_sayisi = len(suan_icerde) 
        ay_giris_sayisi = len(ay_giris)
        bugun_toplam=0 
        ay_toplam = 0
        bugun_bakiye_toplam =0
        ay_bakiye_toplam =0
        for i in bugun_giris:
            bugun_toplam += i.odenen_tutar
        for i in ay_giris:
            ay_toplam += i.odenen_tutar
        for i in bugun_bakiye:
            bugun_bakiye_toplam +=i.yuklenenBakiye
        for i in ay_bakiye:
            ay_bakiye_toplam +=i.yuklenenBakiye

        context={

            'bugun_giris' : bugun_giris,
            'suan_icerde': suan_icerde,
            'ay_giris': ay_giris,
            'bugun_giris_sayisi': bugun_giris_sayisi,
            'suan_icerde_sayisi': suan_icerde_sayisi,
            'ay_giris_sayisi': ay_giris_sayisi,
            'bugun_toplam': bugun_toplam,
            'ay_toplam' : ay_toplam,
            'bugun_bakiye':bugun_bakiye,
            'ay_bakiye':ay_bakiye,
            'bugun_bakiye_toplam':bugun_bakiye_toplam,
            'ay_bakiye_toplam':ay_bakiye_toplam,
        }
        return render(request, 'dashboard.html',context)

    return redirect('aboneApp:login') 

def view_iceridekiler(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        kullanicilar = aktiviteKullanimi.objects.filter(giris_durumunda_mi = True)
        context = {
            "kullanicilar":kullanicilar
        }
        return render(request,"iceridekiler.html",context)

def view_bugun_girenler(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bugun_kullanicilar = aktiviteKullanimi.objects.filter(girdigiZaman__year =today.year,girdigiZaman__month =today.month,girdigiZaman__day =today.day)
        context = {
            "kullanicilar":bugun_kullanicilar
        }
        return render(request,"bugunGirenler.html",context)
    return redirect('aboneApp:login') 

def view_bu_ay_girenler(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bugun_kullanicilar = aktiviteKullanimi.objects.filter(girdigiZaman__year =today.year,girdigiZaman__month =today.month)
        context = {
            "kullanicilar":bugun_kullanicilar
        }
        return render(request,"buAyGirenler.html",context)
    return redirect('aboneApp:login') 

def bugun_tutar(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bugun_giris = aktiviteKullanimi.objects.filter(girdigiZaman__year =today.year,girdigiZaman__month =today.month,girdigiZaman__day =today.day)
        context = {
            "kullanicilar":bugun_giris
        }
        return render(request,"bugunTutar.html",context)
    return redirect('aboneApp:login') 

def bu_ay_tutar(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bugun_giris = aktiviteKullanimi.objects.filter(girdigiZaman__year =today.year,girdigiZaman__month =today.month)
        context = {
            "kullanicilar":bugun_giris
        }
        return render(request,"buAyTutar.html",context)
    return redirect('aboneApp:login') 

def bugun_bakiye(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bugun_bakiye = bakiyeLog.objects.filter(yuklenenZaman__year =today.year,yuklenenZaman__month =today.month,yuklenenZaman__day =today.day)
        context = {
            "kullanicilar":bugun_bakiye
        }
        return render(request,"bugunBakiye.html",context)
    return redirect('aboneApp:login') 

def bu_ay_bakiye(request):
    if request.user.is_authenticated  and request.user.is_superuser:
        today = date.today()
        bu_ay_bakiye = bakiyeLog.objects.filter(yuklenenZaman__year =today.year,yuklenenZaman__month =today.month)
        context = {
            "kullanicilar":bu_ay_bakiye
        }
        return render(request,"buAyBakiye.html",context)
    return redirect('aboneApp:login') 