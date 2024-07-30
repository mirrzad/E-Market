from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Otp


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'full_name')
    list_filter = ('is_superuser',)
    search_fields = ('email', 'full_name')

    ordering = ('full_name',)

    fieldsets = ((None, {'fields': ('phone_number', 'email', 'full_name', 'password')}),
                 ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
                 )
    add_fieldsets = ((None, {'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2')}),
                     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')})
                     )

    filter_horizontal = ()


class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_time')
    list_filter = ('phone_number',)


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Otp, OtpAdmin)
