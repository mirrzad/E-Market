import random
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, CodeVerificationForm, UserLoginForm
from utils.sms_service import send_otp
from .models import Otp, User


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register-user.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_register_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'password': cd['password1']
            }
            otp = Otp.objects.create(
                phone_number=cd['phone_number'],
                code=random.randint(1000, 9999)
            )
            send_otp(otp.phone_number, otp.code)
            messages.success(request, 'We’ve sent a 4-digit code to your phone', 'success')
            return redirect('account:verify-register-code')
        return render(request, self.template_name, {'form': form})


class CodeVerificationRegisterView(View):
    form_class = CodeVerificationForm
    template_name = 'account/code-verification.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_register_info']
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = Otp.objects.filter(phone_number=user_session['phone_number']).first()
            if cd['code'] != code_instance.code:
                messages.error(request, 'Incorrect code', 'danger')
                return redirect('account:verify-register-code')
            elif code_instance.is_expired:
                messages.error(request, 'The code has been expired! Please Try again.', 'danger')
                return redirect('account:user-register')
            else:
                user = User(
                    phone_number=user_session['phone_number'],
                    email=user_session['email'],
                )
                user.set_password(user_session['password'])
                user.save()
                code_instance.delete()
                messages.success(request, 'You registered successfully!', 'success')
                return redirect('home:home-page')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login-user.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are logged In', 'warning')
            return redirect('home:home-page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(phone_number=cd['phone_number'])
            except:
                messages.error(request, 'You should register first!', 'warning')
                return redirect('account:user-register')
            else:
                if user.check_password(cd['password']):
                    request.session['user_login_info'] = {
                        'phone_number': cd['phone_number'],
                        'password': cd['password']
                    }
                    otp = Otp.objects.create(
                        phone_number=cd['phone_number'],
                        code=random.randint(1000, 9999)
                    )
                    send_otp(otp.phone_number, otp.code)
                    messages.success(request, 'We’ve sent a 4-digit code to your phone', 'success')
                    return redirect('account:verify-login-code')
                else:
                    messages.error(request, 'Incorrect username or password!', 'danger')
                    return redirect('account:user-login')
        return render(request, self.template_name, {'form': form})


class CodeVerificationLoginView(View):
    form_class = CodeVerificationForm
    template_name = 'account/code-verification.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_login_info']
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = Otp.objects.filter(phone_number=user_session['phone_number']).first()
            if cd['code'] != code_instance.code:
                messages.error(request, 'Incorrect code', 'danger')
                return redirect('account:verify-login-code')
            elif code_instance.is_expired:
                messages.error(request, 'The code has been expired! Please Try again.', 'danger')
                return redirect('account:user-login')
            else:
                user = User.objects.get(phone_number=user_session['phone_number'])
                login(request, user)
                code_instance.delete()
                messages.success(request, 'You logged in successfully!', 'success')
                return redirect('home:home-page')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are logged out successfully', 'success')
        return redirect('home:home-page')
