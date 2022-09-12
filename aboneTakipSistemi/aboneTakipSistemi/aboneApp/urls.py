from django.urls import path
from . import views

app_name = 'aboneApp'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('kullanicilarlistesi/', views.kullanici_listeleme, name='kullanici_listeleme'),
    path('kullaniciarama/<int:id>/', views.kullanici_arama, name='kullanici_arama'),
    path('rapor/', views.rapor, name='rapor'),
    path('aylik/rapor/', views.aylik_rapor, name='aylik_rapor'),
    path('logout/', views.logout, name='logout'),
    path('ayarlar/<int:id>', views.guncelleFonksiyon, name='guncelleFonksiyon'),
    path('kullaniciSil/<int:id>/', views.sil, name='kullaniciSil'),
    path('kullaniciEkle/', views.kullaniciEkle, name='kullaniciEkle'),
    path('kullanimAlaniListeleme/', views.kullanimAlaniListeleme, name='kullanimAlaniListeleme'),
    path('kullanimAlaniEkle/', views.kullanimAlaniEkle, name='kullanimAlaniEkle'),
    path('bakiyeYuklemeAyarlari/<int:id>/', views.bakiye_yukle, name='bakiye_yukle'),
    path('kullanici_giris/<int:id>/', views.kullanici_giris, name='kullanici_giris'),
    path('kullanici_cikis/<int:id>/', views.kullanici_cikis, name='kullanici_cikis'),
    path('kullanimAlaniGuncellemeAyari/<int:id>/', views.kullanimAlaniGuncelle, name='kullanimAlaniGuncelle'),
    path('kullanimAlanisil/<int:id>/', views.kullanimAlanisil, name='kullanimAlanisil'),
    path('bakiyeRapor/', views.bakiye_raporu, name='bakiye_raporu'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('icerdekiler/', views.view_iceridekiler, name='icerdekiler'),
    path('bugunGirenler/', views.view_bugun_girenler, name='bugunGirenler'),
    path('buAyGirenler/', views.view_bu_ay_girenler, name='buAyGirenler'),
    path('bugunTutar/', views.bugun_tutar, name='bugunTutar'),
    path('buAyTutar/', views.bu_ay_tutar, name='buAyTutar'),
    path('bugunBakiye/', views.bugun_bakiye, name='bugunBakiye'),
    path('buAyBakiye/', views.bu_ay_bakiye, name='buAyBakiye'),
    path('bugununRapor/',views.rapor,name='bugununRapor'),
    path('turnikeEkle/',views.turnikeEkle,name='turnikeEkle'),
    path('turnikeGuncelle/<int:id>/',views.turnike_guncelle,name='turnikeGuncelle'),

]               