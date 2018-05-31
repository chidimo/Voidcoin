from django.db import models

from siteuser.models import SiteUser
from .utils import TimeStampedModel

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
