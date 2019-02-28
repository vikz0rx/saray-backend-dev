import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, timedelta

class SarayUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class SarayUser(AbstractBaseUser, PermissionsMixin):
    BONUS_CLASSIC = "CLASSIC"
    BONUS_SILVER = "SILVER"
    BONUS_GOLD = "GOLD"
    BONUS_PLATINUM = "PLATINUM"

    BONUS_CHOICES = (
        (BONUS_CLASSIC, "Классическая карта"),
        (BONUS_SILVER, "Серебряная карта"),
        (BONUS_GOLD, "Золотая карта"),
        (BONUS_PLATINUM, "Платиновая карта"),
    )

    bonus = models.CharField(_('Бонусная карта'), max_length=32, choices=BONUS_CHOICES, default=BONUS_CLASSIC)
    username = models.CharField(_('Имя пользователя'), db_index=True, max_length=255, unique=True)
    email = models.EmailField(_('Электропочта'), db_index=True, unique=True)
    phone = models.CharField(_('Номер телефона'), max_length=11, null=True, blank=True)
    image = models.FileField(_('Изображение'), upload_to='headshots', null=True, blank=True)
    
    firstname = models.CharField(_('Имя'), max_length=32, null=True, blank=True)
    lastname = models.CharField(_('Фамилия'), max_length=32, null=True, blank=True)
    fathersname = models.CharField(_('Отчество'), max_length=32, null=True, blank=True)

    birthdate = models.DateField(_('Дата рождения'), null=True, blank=True)
    
    passport_series = models.CharField(_('Серия паспорта'), max_length=4, null=True, blank=True)
    passport_number = models.CharField(_('Номер паспорта'), max_length=6, null=True, blank=True)
    insurance = models.CharField(_('СНИЛС'), max_length=11, null=True, blank=True)

    sms_notification = models.BooleanField(_('Оповещение по SMS'), default=False)
    mail_notification = models.BooleanField(_('Оповещение по электропочте'), default=True)
    allow_to_use_photos = models.BooleanField(_('Разрешение на использование фотографий'), default=True)

    is_active = models.BooleanField(_('Активный аккаунт'), default=True)
    is_staff = models.BooleanField(_('Административный аккаунт'), default=False)

    created_at = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = SarayUserManager()

    def __str__(self):
        if self.firstname and self.lastname and self.fathersname:
            return self.firstname + ' ' + self.lastname + ' ' + self.fathersname
        elif self.firstname and self.lastname:
            return self.firstname + ' ' + self.lastname
        else:
            return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    class Meta:
        ordering = ['is_superuser', 'is_staff', '-created_at']
        verbose_name = _('пользователя фотостудии')
        verbose_name_plural = _('Пользователи фотостудии')

class Locations(models.Model):
    title = models.CharField(_('Название локации'), max_length=32)
    text = models.TextField(_('Описание'), max_length=4096)
    image = models.FileField(_('Обложка'), upload_to='locations')
    cost = models.SmallIntegerField(_('Стоимость аренды'), )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('локацию')
        verbose_name_plural = _('Локации')

class Photographs(models.Model):
    first_name = models.CharField(_('Имя'), max_length=32)
    last_name = models.CharField(_('Фамилия'), max_length=32)
    desc = models.CharField(_('Описание'), max_length=64)
    link = models.CharField(_('Instagram'), max_length=64)
    image = models.FileField(_('Фотография'), upload_to='headshots')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('фотографа')
        verbose_name_plural = _('Фотографы')

class News(models.Model):
    author = models.ForeignKey(SarayUser, on_delete=models.CASCADE, related_name='author', blank = True, null = True)
    title = models.CharField(_('Заголовок'), max_length=128)
    text = models.TextField(_('Текст статьи'), max_length=4096)
    image = models.FileField(_('Обложка'), upload_to='news')
    approved = models.BooleanField(_('Одобрено'), default=False)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-approved', '-created_at']
        verbose_name = _('новость')
        verbose_name_plural = _('Новости')

class BookingTypes(models.Model):
    title = models.CharField(_('Название'), max_length=32)
    desc = models.CharField(_('Описание'), max_length=512)
    cost = models.SmallIntegerField(_('Стоимость'), )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('тип бронирования')
        verbose_name_plural = _('Бронирования / Типы бронирования')

class BookingOptions(models.Model):
    title = models.CharField(_('Название'), max_length=32)
    desc = models.CharField(_('Описание'), max_length=512)
    cost = models.SmallIntegerField(_('Стоимость'), )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('дополнительную услугу')
        verbose_name_plural = _('Бронирования / Дополнительные услуги')

class Bookings(models.Model):
    IS_CREATED = "IN_PROGRESS"
    IS_PAYED = "IS_PAYED"

    STATUS_CHOICES = (
        (IS_CREATED, "Не оплачен"),
        (IS_PAYED, "Оплачен"),
    )


    user = models.ForeignKey(SarayUser, on_delete=models.CASCADE, related_name='customer', blank = True, null = True)
    date = models.DateField()
    time_start = models.TimeField(_('Начало'), blank=True, null=True)
    time_end = models.TimeField(_('Конец'), blank=True, null=True)
    status = models.CharField(_('Статус'), max_length=16, choices=STATUS_CHOICES, default=IS_CREATED)
    
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='location')
    photograph = models.ForeignKey(Photographs, on_delete=models.CASCADE, blank=True, related_name='photograph')
    types = models.ForeignKey(BookingTypes, on_delete=models.CASCADE, blank=True, related_name='type')
    options = models.ManyToManyField(BookingOptions, blank=True, related_name='options_choice')

    payment_notification = models.BooleanField(_('Оповещение I'), default=False)
    reminder_notification = models.BooleanField(_('Оповещение II'), default=False)

    cost = models.SmallIntegerField(_('Стоимость'), blank=True, null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ['-status', '-date']
        verbose_name = _('бронирование')
        verbose_name_plural = _('Бронирования')

# IS_PAYED = "IS_PAYED"
# IN_PROGRESS = "IN_PROGRESS"
# IS_DONE = "IS_DONE"

# STATUS_CHOICES = (
#     (IS_PAYED, "Оплачен"),
#     (IN_PROGRESS, "Выполняется"),
#     (IS_DONE, "Завершен"),
# )

# status = models.CharField(_('Статус'), max_length=16, choices=STATUS_CHOICES, default=IS_PAYED)