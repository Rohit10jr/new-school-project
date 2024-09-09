
from django.urls import path

from accounts.views import SignupView
from .frontendviews import *


urlpatterns=[
    path('',land,name='land'),
    path('home/',home,name='home'),
    path('signup/',signup,name='signup'),
    path('login/',simple,name='simple'),
    path('profile/',profile,name='profile'),
     path('students/',students,name='userdetails'),
     path('staffs/',staff,name='staff'),
     path('404',unknown),
     path('index',index)
]