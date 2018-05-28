# from django.core.files import File
import json
from random import randint

import requests

from django.template.defaultfilters import slugify

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import SiteUser

CustomUser = get_user_model()

login_backends = {}
login_backends['django'] = 'django.contrib.auth.backends.ModelBackend'
login_backends['twitter'] = 'social_core.backends.twitter.TwitterOAuth'
login_backends['google_oauth2'] = 'social_core.backends.google.GoogleOAuth2'
login_backends['facebook'] = 'social_core.backends.facebook.FacebookOAuth2'
login_backends['yahoo'] = 'social_core.backends.yahoo.YahooOAuth2'

def save_avatar(image_url, model_object):
    response = requests.get(image_url)
    if response.status_code == 200:
        name = model_object.screen_name.lower()
        model_object.avatar.save(name, ContentFile(response.content), save=True)

def save_social_profile(backend, user, response, *args, **kwargs):
    request = kwargs['request']

    if backend.name == "twitter":
        # with open("response-twitter.json", "w+") as fh:
        #     json.dump(response, fh)
        screen_name = slugify(response['screen_name']) # twitter response contains a screen_name
        image = response['profile_image_url']
        location = response['location']
        name = response['name'].split()
        first_name = name[0]
        try:
            last_name = name[1]
        except IndexError:
            last_name = ''
        email = response.get('email', None)
        if email is None:
            msg = """It appears you have no email set in your twitter account.
            We have created a dummy email {} for you for purpose of registration.
            Please be sure to change it to a real email.""".format(email)
            messages.success(request, msg)
        
        if CustomUser.objects.filter(email=email).exists():
            social_user = CustomUser.objects.get(email=email)
            
            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name=first_name, last_name=last_name, location=location)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

        else:
            social_user = CustomUser.objects.create_user(email=email, password=None)
            social_user.is_active = True
            social_user.save()

            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name=first_name, last_name=last_name, location=location)
                        save_avatar(image, su)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

    elif backend.name == 'google-oauth2':
        # with open("response-google.json", "w+") as fh:
        #     json.dump(response, fh)
        screen_name = slugify(response['displayName'].strip())
        email = response['emails'][0]['value']
        first_name = response['name']['givenName']
        last_name = response['name']['familyName']
        image = response['image']['url'].split('?')[0]
        
        if CustomUser.objects.filter(email=email).exists():
            social_user = CustomUser.objects.get(email=email)
            
            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name=first_name, last_name=last_name)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

        else:
            social_user = CustomUser.objects.create_user(email=email, password=None)
            social_user.is_active = True
            social_user.save()

            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name=first_name, last_name=last_name)
                        save_avatar(image, su)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

    elif backend.name == 'facebook':
        # with open("response-facebook.json", "w+") as fh:
        #     json.dump(response, fh)
        name = response['name'].split()
        first_name = name[0]
        try:
            last_name = name[1]
        except IndexError:
            last_name = ''
        screen_name = slugify("{}-{}".format(first_name, last_name))
        email = response.get('email', None)
        image = 'https://graph.facebook.com/{}/picture?type=large'.format(response['id'])

        if CustomUser.objects.filter(email=email).exists():
            social_user = CustomUser.objects.get(email=email)
            
            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name=first_name, last_name=last_name)
                        save_avatar(image, su)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

        else:
            social_user = CustomUser.objects.create_user(email=email, password=None)
            social_user.is_active = True
            social_user.save()

            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name=first_name, last_name=last_name)
                        save_avatar(image, su)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

    elif backend.name == 'yahoo-oauth2':
        # with open("response-yahoo.json", "w+") as fh:
        #     json.dump(response, fh)
        image = response['image']['imageUrl']
        screen_name = slugify(response['nickname']) # not unique. check for collisions
        email = "{}@yahoo.com".format(response['guid'].lower()) # make email from guid
        msg = """We couldn't find your yahoo mail address so
        We have created a dummy email {} for you for purpose of registration.
        Please be sure to change it to a real email.""".format(email)
        messages.success(request, msg)

        if CustomUser.objects.filter(email=email).exists():
            social_user = CustomUser.objects.get(email=email)
            
            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name='', last_name='')
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}

        else:
            social_user = CustomUser.objects.create_user(email=email, password=None)
            social_user.is_active = True
            social_user.save()

            if SiteUser.objects.filter(user=social_user).exists():
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
            else:
                while True: # keep looping until a SiteUser is successfully created
                    screen_name = "{}{}".format(screen_name, randint(10, 1000)) # append a random string
                    try:
                        su = SiteUser.objects.create(user=social_user, screen_name=screen_name, first_name='', last_name='')
                        save_avatar(image, su)
                        break
                    except IntegrityError:
                        continue
                login(request, social_user, backend=login_backends['django'])
                # return {'username' : screen_name}
