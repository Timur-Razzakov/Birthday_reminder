from ckeditor.widgets import CKEditorWidget
from django.forms import NumberInput
from .models import MailingCommerceOffer, Holiday
from django import forms

from accounts.models import CompanyDetail, City


class HolidayFrom(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Изображение',
        required=False
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Наименование праздника',
    )
    date = forms.DateField(label='Дата праздника',
                           widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'})
                           )
    congratulation = forms.CharField(widget=CKEditorWidget(), label='Поздравление')

    class Meta:
        model = Holiday
        fields = ('image', 'name', 'date', 'congratulation')


class MailingCommerceOfferFrom(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Изображение',
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label='Ссылки ( Если их несколько, то введите через запятую)',
    )

    company_detail = forms.ModelChoiceField(
        queryset=CompanyDetail.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите реквизиты вашей компании'
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите город',
        help_text='Если хотите разослать всем городам, то оставьте поле пустым (-----)',
    )
    message = forms.CharField(
        widget=CKEditorWidget(),
        label='Место для вашего предложения',
    )

    class Meta:
        model = MailingCommerceOffer
        fields = ('image', 'city', 'link', 'company_detail', 'message')
