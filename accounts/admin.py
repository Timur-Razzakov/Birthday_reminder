from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import MyUser, Client, CompanyDetail, Channel, City, Gender


class UserCreationForm(forms.ModelForm):
    """Форма для заполнения пароля и создание пользователя"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

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
        fields = ('email', 'password', 'is_active', 'is_admin')

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
        (None, {'fields': ('email', 'password')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    """ Поля которые будут использоваться при создании пользователя """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(Client)
admin.site.register(CompanyDetail)
admin.site.register(Channel, )
admin.site.register(City, )
admin.site.register(Gender, )
""" отмена регистрацию модели группы от администратора"""
admin.site.unregister(Group)
