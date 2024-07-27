from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logoutuser, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('chat/', views.queries, name='chat'),
    path('trips/', views.trip_list, name='trip_list'),
    path('track/', views.track, name='track'),
    path('about/', views.about, name='about'),
    path('payment/', views.payment, name='payment'),
    path('paymentstatus/',views.payment_status,name='payment-status'),
    path('sud/', views.sud, name='sud'),
    path('sud/<str:pk>/', views.track, name='sud_detail'),
    path('reservation/',views.reservation_view,name='reservation'),
] 
