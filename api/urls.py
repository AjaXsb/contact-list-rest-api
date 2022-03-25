from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adduser', views.adduser.as_view(), name='adduser'),
    path('loginuser', views.loginuser.as_view(), name='loginuser'),

    path('markspam', views.markspam.as_view(), name='markspam'),

    path('namesearch', views.namesearch.as_view(), name='namesearch'),
    path('phonesearch', views.phonesearch.as_view(), name='phonesearch'),
    path('getcontactdetails', views.getcontactdetails.as_view(), name='getcontactdetails'),
    
    path('contactsearch', views.contactsearch.as_view(), name='contactsearch'),
    
    path('global', views.usershow.as_view(), name='users'),
]