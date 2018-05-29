from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import AutoCreatedField, AutoLastModifiedField

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True
