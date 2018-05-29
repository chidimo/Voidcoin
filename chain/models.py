from decimal import Decimal

from django.db import models

from siteuser.models import SiteUser
from .utils import TimeStampedModel

class BlockAccount(TimeStampedModel):
    owner = models.ForeignKey(SiteUser, null=True, blank=True, on_delete=models.CASCADE)
    private_key = models.TextField()
    public_key = models.TextField()
    used = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.owner.__str__() + " key"

    def save(self, *args, **kwargs):
        return super(BlockAccount, self).save(*args, **kwargs)
