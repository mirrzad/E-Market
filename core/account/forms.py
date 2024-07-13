from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Password_Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2 or password1 != password2:
            raise ValidationError('The two password fields don’t match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already exists!')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('This phone_number is already exists!')
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='You can change your password using <a href="../password/"> this form </a>.'
    )

    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[validate_password]
                                )
    password2 = forms.CharField(label='Password_Confirm',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )

    class Meta:
        model = User
        fields = ('phone_number', 'email')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2 or password1 != password2:
            raise ValidationError('The two password fields don’t match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already exists!')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('This phone_number is already exists!')
        return phone_number


class CodeVerificationForm(forms.Form):
    code = forms.IntegerField(label='Insert the code',
                              widget=forms.TextInput(attrs={'class': 'form-control'})
                              )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if len(str(code)) != 4:
            raise ValidationError('Code must have 4-digits')
        return code


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               validators=[validate_password]
                               )

