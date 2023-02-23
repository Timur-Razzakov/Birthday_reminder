from .models import MailingCommerceOffer
from django import forms

"""Форма для объединения страны и ссылки"""


# class GeneralForm(forms.ModelForm):
#

class MailingCommerceOfferFrom(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Номер телефона',
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Адрес',
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Электронный адрес',
    )
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Текст',
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label='Ссылки',
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Текст',
    )

    class Meta:
        model = MailingCommerceOffer
        fields = ('phone_number', 'address',
                  'email', 'link', 'photo', 'text',)
