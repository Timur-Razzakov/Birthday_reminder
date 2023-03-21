from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms

from .models import TemplateForChannel, MailingCommerceOffer, Result, Holiday, MultipleImage


# Register your models here.

class MailingCommerceOfferForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MailingCommerceOffer
        fields = '__all__'


class MailingCommerceOfferAdmin(admin.ModelAdmin):
    form = MailingCommerceOfferForm
    list_display = ('pk', 'link', 'company_detail', 'message', 'created_at')
    filter_horizontal = ('photo',)  # для ManyToMany


class HolidayForm(forms.ModelForm):
    congratulation = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Holiday
        fields = '__all__'


class HolidayFormAdmin(admin.ModelAdmin):
    form = HolidayForm
    list_display = ('id', 'image', 'name', 'date', 'congratulation')


admin.site.register(TemplateForChannel, )
admin.site.register(MailingCommerceOffer, MailingCommerceOfferAdmin)
admin.site.register(Result, )
admin.site.register(MultipleImage, )

admin.site.register(Holiday, HolidayFormAdmin)
