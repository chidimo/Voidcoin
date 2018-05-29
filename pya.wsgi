import os
import sys

path = '/home/parousia/voidcoin'
if path not in sys.path:
    sys.path.append(path)

# set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'voidcoin.settings.prod'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'www.parousia.pythonanywhere.com'
os.environ['SECRET_KEY'] = '-yj%bb6h89%&)&(=%didix35(gaag1&f*$73+=h5b3=v-1uy*p'
os.environ['DJANGO_ADMIN_URL'] = '/admin/'

# os.environ['DATABASE_URL'] = 'mysql://parousia:chinekeIGWEna474@parousia.mysql.pythonanywhere-services.com/parousia$koboland'
# os.environ['KOBOLAND_PASS'] = 'chinekeIGWEna474'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
