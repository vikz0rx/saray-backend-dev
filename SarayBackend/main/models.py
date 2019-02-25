from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
import jwt

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
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = SarayUserManager()

    def __str__(self):
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
        ordering = ['-created_at']
        verbose_name_plural = _('Пользователи')

class Locations(models.Model):
    title = models.CharField(max_length=32)
    text = models.TextField(max_length=4096)
    image = models.FileField(upload_to='locations')
    cost = models.SmallIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('локация')
        verbose_name_plural = _('Локации')

class Photographs(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    desc = models.CharField(max_length=64)
    link = models.CharField(max_length=64)
    image = models.FileField(upload_to='photographs')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('фотограф')
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
        ordering = ['-created_at']
        verbose_name = _('новость')
        verbose_name_plural = _('Новости')