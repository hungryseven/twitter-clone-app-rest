from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_name', 'about', 'location', 'website', 'date_of_birth', 'is_staff', 'is_active')

class CustomUserAdmin(UserAdmin):
    '''
    Класс, представляющий админ-панель для модели пользователей.
    '''

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'profile_name', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'profile_name')
    search_help_text = 'Поиск по имени пользователя, email или имени профиля'
    readonly_fields = (
        'about', 'location', 'website', 'date_joined'
    )
    show_full_result_count = False
    ordering = ('pk',)
    fieldsets = (
        ('Персональные данные', {
            'fields': ('username', 'email', 'password')
            }
        ),
        ('Персональная информация', {
            'fields': ('profile_name', 'about', 'location', 'website', 'date_of_birth', 'date_joined')
            }
        ),
        ('Разрешения', {
            'fields': ('is_staff', 'is_active')
            }
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'profile_name', 'date_of_birth', 'password1', 'password2'),
            }
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_title = 'Twitter'
admin.site.site_header = 'Twitter'
