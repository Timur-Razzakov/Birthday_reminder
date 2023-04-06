from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .forms import ClientForm, CompanyDetailForm
from .models import MyUser, Client, CompanyDetail, Channel, City, Gender


class UserCreationForm(forms.ModelForm):
    """Форма для заполнения пароля и создание пользователя"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    user_name = forms.CharField(label='User name (telegram_nickname) ', widget=forms.TextInput)

    class Meta:
        model = MyUser
        fields = ('email', 'user_name')

    def clean_password2(self):
        """Проверяет пароли на совпадение между собой"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """ Производим сохранение пользователя """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'user_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Независимо от того, что предоставил пользователь, вернуть начальное значение.
        # Это делается здесь, а не на поле, потому что
        # поле не имеет доступа к начальному значению
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # Формы для добавления и изменения пользовательских экземпляров
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'id', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        # Поля для Отображения в админке
        (None, {'fields': ('email', 'password', 'user_name')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    """ Поля которые будут использоваться при создании пользователя """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ClientAdmin(admin.ModelAdmin):
    form = ClientForm
    list_display = ('first_name', 'father_name', 'date_of_birth', 'phone_number', 'pk',)


class CompanyDetailAdmin(admin.ModelAdmin):
    form = CompanyDetailForm
    list_display = ('name', 'email', 'phone_number', 'pk',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk',)


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk',)


class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk',)


admin.site.register(MyUser, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(CompanyDetail, CompanyDetailAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Gender, GenderAdmin)
""" отмена регистрацию модели группы от администратора"""
admin.site.unregister(Group)
