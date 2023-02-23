from django.contrib import admin

from .models import Channel, TemplateForChannel, MailingCommerceOffer, CongratulateClient, Result

# Register your models here.

admin.site.register(Channel, )
admin.site.register(TemplateForChannel, )
admin.site.register(MailingCommerceOffer, )
admin.site.register(CongratulateClient, )
admin.site.register(Result, )
