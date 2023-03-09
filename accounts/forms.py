from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.forms import NumberInput

from .models import Client, CompanyDetail, City, Gender

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    """ Проверка на валидацию"""

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не верный!')
            # проверяем существует ли пользователь
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class CityFrom(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Наименование города',
    )

    class Meta:
        model = City
        fields = ('name',)


class ClientForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия',
    )
    father_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Отчество',
    )
    date_of_birth = forms.DateField(label='Дата рождения',
                                    widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'})
                                    )
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Пол человека',
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Электронная почта',
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефона',
    )
    international_passport = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Загран паспорт',
    )
    national_passport = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Местный паспорт',
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Адрес проживания',
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите город проживания',
    )

    class Meta:
        model = Client
        fields = (
            'first_name', 'last_name', 'father_name', 'date_of_birth', 'gender',
            'international_passport', 'national_passport', 'email', 'address',
            'phone_number')


class CompanyDetailForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Наименовании компании',
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Электронная почта',
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефона',
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Адрес',
    )
    web_site = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Ссылка на веб-сайт',
    )
    company_motto = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Девиз компании',
    )

    class Meta:
        model = CompanyDetail
        fields = ('name', 'phone_number', 'email',
                  'address', 'web_site', 'company_motto')


class SearchClientForm(forms.Form):
    """Форма для поиска клиентов"""
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='ФИО',
        required=False
    )
    date_of_birth = forms.DateField(label='Дата рождения',
                                    widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'}),
                                    required=False
                                    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Электронная почта',
        required=False
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите город проживания',
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефона',
        required=False
    )

    class Meta:
        model = Client
        fields = (
            'full_name', 'city', 'date_of_birth', 'email', 'phone_number')
