from urllib import response
from . forms import *
from re import sub
from django.contrib.auth import login,logout
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import decorator_from_middleware


# def user(request,email,phone):
#     user= User.objects.get(email=email,phone=phone)
#     if user:
#         login(request,user)
        
# def land(request):
#     return render(request,'accounts/content.html')

# def home(request):
#     return render(request,'base.html')

# def signup(request): 
#     form=signup_form(data=request.POST)    
#     return render(request,'accounts/signup.html',{'form':form})  

# def simple(request):      
#     form=login_form()
#     return render(request,'accounts/login.html',{'form':form})

# def profile(request): 
#     print(request.user,'hi')
#     return render(request,'accounts/profile.html')

# def students(request):
#     return render(request,'accounts/students.html')

# def staff(request):
#     return render(request,'accounts/staffs.html')

# def index(request):
#     return render(request,'index.html')


# def logoutview(request):
#     return redirect ('/login/')


def signup_page(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')

# @login_required
def home_page(request):
    return render(request, 'home.html')

def logout_view(request):
    # # Log the user out from the session
    # logout(request)
    # # Redirect to login page
    # return redirect('login')  # Make sure 'login' is the name of your login URL
    return render(request, 'logout.html')

# custom 404 view / learn
# def custom_404_view(request, exception=None):
#     return render(request, '404.html', status=404)


def profile(request): 
    print(request.user,'hi')
    return render(request,'profile.html')