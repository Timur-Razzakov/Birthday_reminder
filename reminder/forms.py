from .models import MailingCommerceOffer, Holiday
from django import forms

from accounts.models import CompanyDetail

"""Форма для объединения страны и ссылки"""


# class GeneralForm(forms.ModelForm):
#
class HolidayFrom(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Наименование праздника',
    )
    date = forms.DateField(label='Дата праздника',
                           input_formats=['%d.%m.%Y', '%Y.%m.%d'],
                           widget=forms.DateInput(attrs={'class': 'form-control'}),
                           )
    clients = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Пол человека',
    )

    class Meta:
        model = Holiday
        fields = ('name', 'date', 'clients')


class MailingCommerceOfferFrom(forms.ModelForm):
    photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Текст',
    )

    link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label='Ссылки ( Если их несколько, то введите через запятую)',
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Место для вашего предложения',
    )
    company_detail = forms.ModelChoiceField(
        queryset=CompanyDetail.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите реквизиты вашей компании'
    )

    class Meta:
        model = MailingCommerceOffer
        fields = ('photo', 'link', 'company_detail', 'message',)
