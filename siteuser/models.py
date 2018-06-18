"""Models"""

from django.db import models
from django.urls import reverse
from django.conf import settings
# from django.contrib.auth.models import Group
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from .utils import TimeStampedModel
from .utils import AutoSlugField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    is_active = models.BooleanField(default=False) # activate by email
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return "User - {}".format(self.email)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def prof(self):
        return self.siteuser.screen_name

class SiteUser(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = AutoSlugField(set_using="screen_name")
    screen_name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['screen_name']
        verbose_name_plural = 'siteusers'

    def __str__(self):
        return self.screen_name

    def get_absolute_url(self):
        return reverse('siteuser:library', args=[str(self.id), str(self.slug)])

    def get_user_success_url(self):
        return reverse()

    def get_user_creation_url(self):
        return reverse('siteuser:new_activation', args=[str(self.user.id), str(self.screen_name)])

class Wallet(TimeStampedModel):
    alias = models.CharField(max_length=30)
    owner = models.ForeignKey(SiteUser, null=True, blank=True, on_delete=models.CASCADE)
    private_key = models.TextField()
    public_key = models.TextField()
    used = models.FloatField(default=0.00)
    balance = models.FloatField(default=0.00)

    def __str__(self):
        return self.owner.__str__() + " - " + self.alias

    def save(self, *args, **kwargs):
        return super(Wallet, self).save(*args, **kwargs)

