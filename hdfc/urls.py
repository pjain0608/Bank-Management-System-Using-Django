from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('1/', views.open, name='open'),
    path('2/', views.transfer, name='transfer'),
    path('3/', views.credit, name='credit'),
    path('4/', views.debit, name='debit'),
    path('5/', views.balance, name='balance'),
    path('6/', views.pin, name='pin'),
    path('7/',views.display, name='display')
]