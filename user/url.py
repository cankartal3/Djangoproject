from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('rehberler/', views.rehberler, name='rehberler'),
    path('rehberekle/', views.rehberekle, name='rehberekle'),
    path('editrehber/<int:id>/', views.editrehber, name='editrehber'),
    path('deleterehber/<int:id>/', views.deleterehber, name='deleterehber'),
    path('rehberaddimage/<int:id>', views.productaddimage, name='productaddimage'),
    path('mesajlar/', views.mesajlar ,name='mesajlar'),
]