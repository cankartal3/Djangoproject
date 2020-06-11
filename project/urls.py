"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path('home/', include('home.urls')),
    path('turistikmekan/', include('turistikmekan.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('home.urls')),
    path('user/', include('user.url')),

    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('referanslarimiz/', views.referanslarimiz, name='referanslarimiz'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('category/<int:id>/<slug:slug>/', views.category_products, name='category_products'),
    path('turistikmekan/<int:id>/<slug:slug>/',views.product_detail, name='product_detail'),
    path('turistikmekan/<int:id>/',views.product_detail_noslug, name='product_detail_noslug'),

    path('search/', views.product_search, name='product_search'),
    path('search_auto/', views.get_places, name='get_places'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    #path('bossayfa/<int:id>/', views.bossayfa , name='bossayfa'),
    path('error/', views.error, name='error'),
    path('onay-bekleyen-icerik/', views.onaybekleyenicerik, name='onaybekleyenicerik'),
    path('sss/', views.faq, name='faq'),
    path('visitetouser/<int:id>', views.visitetouser, name='visitetouser'),
    path('yurtici-turistik-mekanlar/',views.yurticituristikmekanlar, name='yurticituristikmekanlar' ),
    path('yurtdisi-turistik-mekanlar/', views.yurtdisituristikmekanlar, name='yurtdisituristikmekanlar'),
    path('sifremi-unuttum/', views.sifreunuttum, name='sifreunuttum'),

]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)