from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class CompanyDetail(models.Model):
    """Модель, информации о компании"""

    name = models.CharField(max_length=100, verbose_name='company_name')
    address = models.CharField(max_length=255, verbose_name='address')
    phone_number = models.CharField(max_length=13, verbose_name='phone_number',
                                    null=True, blank=True)
    email = models.CharField(max_length=200, verbose_name='email',
                             null=True, unique=True, blank=True)

    def __str__(self):
        return "%i, %s %s" % (self.pk, self.name, self.phone_number)


class Client(models.Model):
    """Модель о Клиентах"""

    phone_number_validator = RegexValidator(
        regex=r'^(\+998|998)?[\s\-]?[0-9]{2}[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        message="""Телефон передается в стандартном формате 
                                           +998|998 xx xxx xx xx (X - от 0 до 10)""")
    email_validator = RegexValidator(
        regex=r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$",
        message="Почта неверного формата")

    chart_id = models.CharField(max_length=10, verbose_name='chart_id', blank=True, null=True)
    user_name = models.CharField(max_length=100, verbose_name='user_name', blank=True, null=True)
    email = models.CharField(max_length=200, verbose_name='email', unique=True,
                             validators=[email_validator], null=True, blank=True)
    phone_number = models.CharField(max_length=13, verbose_name='phone_number',
                                    validators=[phone_number_validator], null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='first_name')
    last_name = models.CharField(max_length=100, verbose_name='last_name')
    date_of_birth = models.DateField(verbose_name='date_of_birth')
    gender = models.CharField(max_length=6)
    address = models.CharField(max_length=255, verbose_name='address')
    traveled = models.TextField(verbose_name='Текст', blank=True, null=True)

    def __str__(self):
        return "%i, %s %s" % (self.pk, self.first_name, self.chart_id)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Создаёт пользователя с указанным email-лом и паролем
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)  # зашифровывает пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Создаёт супер пользователя для доступа к админке
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """проверяет есть ли у пользователя указанное разрешение """
        return True

    def has_module_perms(self, app_label):
        """есть  ли у пользователя разрешение на доступ к моделям в данном приложении. """
        return True

    @property
    def is_staff(self):
        """ Является ли пользователь администратором """
        return self.is_admin
