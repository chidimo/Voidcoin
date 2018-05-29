
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from pywebber import LoremPysum

from siteuser.models import SiteUser

CustomUser = get_user_model()


def superuser():
    try:
        su = CustomUser.objects.create_user(email='admin@voidcoin.net', password='dwarfstar')
        su.is_superuser = True
        su.is_admin = True
        su.is_active = True
        su.save()
    except IntegrityError:
        su = CustomUser.objects.get(email='admin@voidcoin.net')
    try:
        SiteUser.objects.create(
            user=su,
            screen_name="Chidi-Orji",
        )
    except IntegrityError:
        pass

def users():
    n = int(input("Enter number of users to create: "))

    for _ in range(n):
        lorem = LoremPysum()
        email = lorem.email()+str(n)
        try:
            user = CustomUser.objects.create_user(email=email)
            user.set_password("dwarfstar")
            user.is_active = True
            user.save()

            screen_name = lorem.word()

            try:
                SiteUser.objects.create(
                    user=user,
                    screen_name=screen_name,
                    )
            except IntegrityError:
                SiteUser.objects.create(
                    user=user,
                    screen_name=screen_name,
                    )
        except IntegrityError:
            continue
