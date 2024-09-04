from django.urls import path
from .views import SignupView, SimpleLoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('logout/', LogoutView.as_view()),
    path('signup/', csrf_exempt(SignupView.as_view())),
    path('simplelogin/', csrf_exempt(SimpleLoginView.as_view())),
    # path('login/', LoginView.as_view()),

    path('student-profile/<int:pk>/', StudentProfileView.as_view()),
    # path('student-profile/<int:pk>/', csrf_exempt(StudentProfileView.as_view())),
    path('user-details/', UserDetailsView.as_view()),
    path('user-details/<int:pk>/', UserDetailsEditView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('check-user/', check_for_user.as_view()),
    # path('check-user/', csrf_exempt(check_for_user.as_view())),

]