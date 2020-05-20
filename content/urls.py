from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcommentcontent/<int:id>',views.addcommentcontent, name='addcommentcontent'),
]