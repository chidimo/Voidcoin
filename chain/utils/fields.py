from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

class AutoSlugField(models.SlugField):
    """
    A slug field that generates its value from another field
    """
    description = _("Slug field that generates its value from another field on same model")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        set_using = kwargs.pop('set_using', None)
        set_once = kwargs.pop('set_once', True)

        if not set_using:
            raise ImproperlyConfigured(
                '%s requires a field for "set_using"'% self.__class__.__name__
            )
        self.set_using = set_using

        if not isinstance(set_once, bool):
            raise TypeError(
                'The value of "set_once" must be either "True" or "False"'
            )
        self.set_once = set_once
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def get_set_using_field_value(self, instance):
        return getattr(instance, self.set_using)

    def pre_save(self, model_instance, add):
        value = slugify(self.get_set_using_field_value(model_instance))

        if self.set_once:
            if getattr(model_instance, self.attname): #slug field already has a value
                pass
            else:
                setattr(model_instance, self.attname, value)
        else:
            setattr(model_instance, self.attname, value)

        return super(AutoSlugField, self).pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super(AutoSlugField, self).deconstruct()
        kwargs['set_using'] = self.set_using
        kwargs['set_once'] = self.set_once
        return name, path, args, kwargs

class AutoMultipleSlugField(models.SlugField):
    """
    A slug field that generates its value from a list of fields
    """
    description = _("Slug field that generates its value from a list of fields on the same model")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        set_using = kwargs.pop('set_using', [])
        set_once = kwargs.pop('set_once', True) # defaults to empty list

        if not set_using:
            raise ImproperlyConfigured(
                '%s requires at least one field for "set_using"'% self.__class__.__name__
            )

        if not any([isinstance(set_using, list), isinstance(set_using, tuple)]):
            raise TypeError(
                'The value of "set_using" must be of type list or tuple'
            )
        self.set_using = set_using

        if not isinstance(set_once, bool):
            raise TypeError(
                'The value of "set_once" must be either "True" or "False"'
            )
        self.set_once = set_once

        super(AutoMultipleSlugField, self).__init__(*args, **kwargs)

    def get_set_using_field_value(self, instance):
        return " ".join([getattr(instance, each) for each in self.set_using])

    def pre_save(self, model_instance, add):
        value = slugify(self.get_set_using_field_value(model_instance))

        if self.set_once:
            if getattr(model_instance, self.attname): #slug field already has a value
                pass
            else:
                setattr(model_instance, self.attname, value)
        else:
            setattr(model_instance, self.attname, value)

        return super(AutoMultipleSlugField, self).pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super(AutoMultipleSlugField, self).deconstruct()
        kwargs['set_using'] = self.set_using
        kwargs['set_once'] = self.set_once
        return name, path, args, kwargs

# https://github.com/jazzband/django-model-utils
class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.
    By default, sets editable=False, default=datetime.now.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)

class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.
    By default, sets editable=False and default=datetime.now.
    """
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value