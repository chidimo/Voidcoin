from decimal import Decimal

from django.db import models

from siteuser.models import SiteUser
from .utils import TimeStampedModel

class UserKeys(TimeStampedModel):
    owner = models.ForeignKey(SiteUser, null=True, blank=True, on_delete=models.CASCADE)
    private_key = models.CharField(max_length=500)
    public_key = models.CharField(max_length=2000)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
