from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('create_room/', views.create_room, name='create_room'),
    path('<str:room_name>/<str:username>/', views.RoomView, name='room'),

]