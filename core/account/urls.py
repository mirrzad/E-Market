from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('verify_register_code/', views.CodeVerificationRegisterView.as_view(), name='verify-register-code'),
    path('verify_login_code/', views.CodeVerificationLoginView.as_view(), name='verify-login-code'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
]
