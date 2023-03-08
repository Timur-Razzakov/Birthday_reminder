from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms

from .models import TemplateForChannel, MailingCommerceOffer, Result, Holiday


# Register your models here.

class MailingCommerceOfferForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MailingCommerceOffer
        fields = '__all__'


class MailingCommerceOfferAdmin(admin.ModelAdmin):
    form = MailingCommerceOfferForm
    list_display = ('pk', 'photo', 'link', 'company_detail', 'message', 'sending_status', 'created_at')


admin.site.register(TemplateForChannel, )
admin.site.register(MailingCommerceOffer, MailingCommerceOfferAdmin )
admin.site.register(Result, )
admin.site.register(Holiday, )
