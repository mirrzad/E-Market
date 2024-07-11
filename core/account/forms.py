from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password_Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2 or password1 != password2:
            raise ValidationError('The two password fields didn’t match', code="password_mismatch")

        return password2

    def clean(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters!', code="password_too_short")

        return super().clean()

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
