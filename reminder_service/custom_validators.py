from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


GENDER = (
    ('', ''),
    ('Мужчина', 'Мужчина'),
    ('Женщина', 'Женщина'),
)
HOLIDAY = (
    ('', ''),
    ('День рождение', 'День рождение'),
    ('Новый год', 'Новый год'),
    ('Навруз', 'Навруз'),
    ('День почестей', 'День почестей'),
    ('День Независимости', 'День Независимости'),
    ('День конституции', 'День конституции'),
    ('Рамазан Хайит', 'Рамазан Хайит'),
    ('Курбан Хайит', 'Курбан Хайит'),
    ('Международный день туризма', 'Международный день туризма'),
    ('8 марта', '8 марта'),
)

def phone_validator(phone_number):
    regex = r'^(\+998|998)?[\s\-]?[0-9]{2}[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',

    message = """Телефон передается в стандартном формате 
                                       +998|998 xx xxx xx xx (X - от 0 до 10)"""
    if phone_number == regex:
        raise ValidationError(message)

#
# def email_validator(email):
#     email = EmailValidator(
#         regex=r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$",
#         message="Почта неверного формата")
#     return email
