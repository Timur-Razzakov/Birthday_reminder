from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError
from django.forms import NumberInput

from accounts.models import CompanyDetail, City, Gender
from .models import MailingCommerceOffer, Holiday


class HolidayFrom(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Наименование праздника',
    )
    date = forms.DateField(label='Дата праздника',
                           required=True,
                           widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'})
                           )
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Выберите нужный пол'
    )
    congratulation = forms.CharField(widget=CKEditorWidget(),
                                     label='Поздравление')  # max_file_size=1024 * 1024 * 5

    class Meta:
        model = Holiday
        fields = ('image', 'name', 'date', 'gender', 'congratulation')


class MailingCommerceOfferFrom(forms.ModelForm):
    link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label='Ссылки ( Если их несколько, то введите через запятую)',
        required=False
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
        required=False,
        help_text='Если хотите разослать всем городам, то оставьте поле пустым (-----)',
    )
    message = forms.CharField(
        widget=CKEditorWidget(),
        label='Место для вашего предложения',
    )

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, )

    class Meta:
        model = MailingCommerceOffer
        fields = ['images', 'city', 'link', 'company_detail', 'message']

    # для отображения изображений (ManyToMany)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # получаем список ID изображений, связанных с текущей моделью
            self.fields['images'].initial = self.instance.photo.values_list('id',
                                                                            flat=True)
