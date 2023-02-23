from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Client

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


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Введите email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль ещё раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


class ClientForm(forms.ModelForm):
    GENDER = (
        ('', ''),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилию',
    )
    date_of_birth = forms.DateField(label='Дата рождения',
                                    input_formats=['%d.%m.%Y', '%Y.%m.%d'],
                                    widget=forms.DateInput(attrs={'class': 'form-control'}),
                                    )
    chart_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='ID клиента (телеграмм)',
    )
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя пользователя (телеграмм)',
    )
    gender = forms.CharField(
        widget=forms.Select(choices=GENDER, attrs={'class': 'form-control'}),
        label='Пол человека',
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Электронный адрес',
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефона',
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Текст',
    )

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'chart_id',
                  'user_name', 'date_of_birth', 'gender', 'email', 'phone_number', 'text')
