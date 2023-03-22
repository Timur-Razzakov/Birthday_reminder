from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models

from reminder_service import custom_validators


class Gender(models.Model):
    name = models.CharField(verbose_name='GENDER', max_length=7)

    def __str__(self):
        return self.name


class City(models.Model):
    """Модель для всех городов Узбекистана"""
    name = models.CharField(verbose_name='City_name', max_length=255)

    def __str__(self):
        return self.name


class Channel(models.Model):
    """Модель для каналов отправки сообщений и рассылок"""

    name = models.CharField(verbose_name='channel_name', max_length=255)

    def __str__(self):
        return self.name


class CompanyDetail(models.Model):
    """Модель, информации о компании"""
    name = models.CharField(max_length=100, verbose_name='company_name', unique=True)
    address = models.CharField(max_length=255, verbose_name='address')
    phone_number = models.CharField(max_length=13, verbose_name='phone_number',
                                    validators=[custom_validators.phone_validator])
    email = models.CharField(max_length=200, verbose_name='email',
                             validators=[EmailValidator(message='Почта неверного формата!!')],
                             null=True, blank=True)
    web_site = models.URLField(max_length=200, verbose_name='url',
                               null=True, blank=True)
    company_motto = models.CharField(max_length=255, verbose_name='company_motto',
                                     null=True, blank=True)
    logo = models.ImageField(verbose_name='Логотип Компании', upload_to='logo/', blank=True)

    def __str__(self):
        return "%s" % (self.name,)


class Client(models.Model):
    """Модель о Клиентах"""
    full_name = models.CharField(max_length=100, verbose_name='full_name', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='first_name')
    last_name = models.CharField(max_length=100, verbose_name='last_name')
    father_name = models.CharField(max_length=255, verbose_name='father_name')

    email = models.CharField(max_length=200, verbose_name='email',
                             unique=True,
                             validators=[EmailValidator(message='Почта неверного формата')],
                             null=True, blank=True)
    phone_number = models.CharField(max_length=13, verbose_name='phone_number',
                                    validators=[custom_validators.phone_validator], null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='date_of_birth')
    inter_passport = models.CharField(max_length=9, verbose_name='international passport',
                                      validators=[custom_validators.passport_validator])
    passport = models.CharField(max_length=9, verbose_name='national passport',
                                validators=[custom_validators.passport_validator])
    gender = models.ForeignKey(Gender, verbose_name='GENDER', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name='address')
    city = models.ForeignKey(City, verbose_name='City', on_delete=models.CASCADE, null=True,
                             blank=True)
    channel = models.ForeignKey(Channel, verbose_name='channel', on_delete=models.CASCADE, null=True,
                                blank=True, default=1)
    traveled = models.TextField(verbose_name='Текст', blank=True, null=True)

    def __str__(self):
        return str(self.phone_number)


class MyUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
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
    user_name = models.CharField(max_length=100, verbose_name='user_name', unique=True, )
    list_display = ('email', 'is_admin', 'user_name')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Проверяет есть ли у пользователя указанное разрешение """
        return True

    def has_module_perms(self, app_label):
        """Есть ли у пользователя разрешение на доступ к моделям в данном приложении. """
        return True

    @property
    def is_staff(self):
        """ Является ли пользователь администратором """
        return self.is_admin
