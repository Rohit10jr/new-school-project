from django.urls import path
from accounts.views import SignupView
from .frontendViews import *


urlpatterns=[
    # path('signup/',signup,name='signup'),
    # path('login/',simple,name='simple'),
    # path('404',unknown),

    # path('home/',home,name='home'),
    # path('',land,name='land'),
    # path('index',index)

# --------------------------------------------

    # path('profile/',profile,name='profile'),
    # path('students/',students,name='userdetails'),
    # path('staffs/',staff,name='staff'),

    path('login/', login_page, name='login'),
    path('signup/', signup_page, name="signup"), 
    path('logout/', logout_view, name="logout"), 
    path('home/', home_page, name='home'),

    # path('register/', signup, name="register"),
    # path('', unknown),

    path('profile/',profile,name='profile'),
    path('students/',students,name='userdetails'),
    path('staffs/',staff,name='staff'),
]
