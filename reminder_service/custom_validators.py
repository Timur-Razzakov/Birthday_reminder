import re

from django.core.exceptions import ValidationError

TEMPLATE_NAME = (
    ('', ''),
    ('Коммерческое предложение', 'Коммерческое предложение'),
    ('День рождения', 'День рождения'),
    ('Праздники', 'Праздники'),
)


# GENDER = (
#     ('', ''),
#     ('Мужчина', 'Мужчина'),
#     ('Женщина', 'Женщина'),
# )
# HOLIDAY = (
#     ('', ''),
#     ('День рождение', 'День рождение'),
#     ('Новый год', 'Новый год'),
#     ('Навруз', 'Навруз'),
#     ('День почестей', 'День почестей'),
#     ('День Независимости', 'День Независимости'),
#     ('День конституции', 'День конституции'),
#     ('Рамазан Хайит', 'Рамазан Хайит'),
#     ('Курбан Хайит', 'Курбан Хайит'),
#     ('Международный день туризма', 'Международный день туризма'),
#     ('8 марта', '8 марта'),
# )


def phone_validator(phone_number: str):
    regex = r'^(\+998|998)?[\s\-]?[0-9]{2}[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'

    message = """Телефон передается в стандартном формате 
                                       +998|998 xx xxx xx xx (X - от 0 до 10)"""
    if not bool(re.fullmatch(regex, phone_number)):
        raise ValidationError(message)


#
# def email_validator(email):
#     email = EmailValidator(
#         regex=r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$",
#         message="Почта неверного формата")
#     return email

def passport_validator(value):
    regex = r'^[a-zA-Z]{2}[0-9]{7}$'
    message = 'Неверный формат паспортных данных'
    if not bool(re.fullmatch(regex, value)) and len(value) != 9:
        raise ValidationError(message)
