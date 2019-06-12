
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from siteuser.models import SiteUser

CustomUser = get_user_model()


def superuser():
    try:
        su = CustomUser.objects.create_user(email='orjichidi95@gmail.com', password='dwarfstar')
        su.is_superuser = True
        su.is_admin = True
        su.is_active = True
        su.save()
    except IntegrityError:
        su = CustomUser.objects.get(email='orjichidi95@gmail.com')
    try:
        SiteUser.objects.create(
            user=su,
            screen_name="Chidi-Orji",
        )
    except IntegrityError:
        pass
