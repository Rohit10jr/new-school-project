from django.urls import path
from .views import SignupView, SimpleLoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('logout/', LogoutView.as_view()),
    path('signup/', csrf_exempt(SignupView.as_view())),
    path('simplelogin/', csrf_exempt(SimpleLoginView.as_view())),
    # path('login/', LoginView.as_view()),

]