from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import TemplateForChannel, MailingCommerceOffer, Result, Holiday, MultipleImage


# Register your models here.

class MailingCommerceOfferForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MailingCommerceOffer
        fields = '__all__'


class MailingCommerceOfferAdmin(admin.ModelAdmin):
    form = MailingCommerceOfferForm
    list_display = ('company_detail', 'message', 'created_at', 'pk', 'link',)
    filter_horizontal = ('photo',)  # для ManyToMany


class HolidayForm(forms.ModelForm):
    congratulation = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Holiday
        fields = '__all__'


class HolidayFormAdmin(admin.ModelAdmin):
    form = HolidayForm
    list_display = ('name', 'date', 'congratulation', 'id', 'image',)


class TemplateForChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel', 'gender', 'templates_for_massage', 'id',)


class ResultAdmin(admin.ModelAdmin):
    list_display = ('sending_status', 'created_at', 'image', 'process_date', 'channels', 'id',)


admin.site.register(TemplateForChannel, TemplateForChannelAdmin)
admin.site.register(MailingCommerceOffer, MailingCommerceOfferAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(MultipleImage, )

admin.site.register(Holiday, HolidayFormAdmin)
