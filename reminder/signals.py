# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from jinja2 import Template
#
# from accounts.models import CompanyDetail
# from reminder.models import MailingCommerceOffer, TemplateForChannel
#
# """Слушаем модель MailingCommerceOffer и если есть новые данные, то запускаем эту функцию"""
#
#
# @receiver(post_save, sender=MailingCommerceOffer)
# def my_handler(sender, instance, **kwargs):
#     """Функция, для получения с моделей данных и обработали их в шаблонах, затем сохраняем"""
#     if kwargs.get('created', False):
#         # создаём итоговый вариант используя шаблон сообщений и сохраняем в модель
#
#         create_mailing = FinalMailingCommerce.objects.create()
#         template = TemplateForChannel.objects.get(name__icontains='предложение')
#         mailing_message = Template(template.templates_for_massage)
#         company_data = CompanyDetail.objects.filter(name=instance.company_detail).values(
#             'address',
#             'name',
#             'phone_number',
#             'email',
#             'web_site',
#             'company_motto',
#             'logo')
#         for item in company_data:
#             msg = mailing_message.render(photo=instance.photo,
#                                          message=instance.message,
#                                          link=instance.link,
#                                          name=item['name'],
#                                          address=item['address'],
#                                          phone_number=item['phone_number'],
#                                          email=item['email'],
#                                          web_site=item['web_site'],
#                                          company_motto=item['company_motto'],
#                                          logo=item['logo'],
#                                          mailing=instance.id
#                                          )
#         print(msg)
#         create_mailing.message = msg
#         create_mailing.save()

