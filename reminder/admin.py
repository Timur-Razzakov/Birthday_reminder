from django.contrib import admin

from .models import TemplateForChannel, MailingCommerceOffer, Result, Holiday

# Register your models here.


admin.site.register(TemplateForChannel, )
admin.site.register(MailingCommerceOffer, )
admin.site.register(Result, )
admin.site.register(Holiday, )
