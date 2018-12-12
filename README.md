# Add [Travis CI](https://travis-ci.com/JBthePenguin/TestTravisCI) to the Django project [PurbeurreWebApp](https://github.com/JBthePenguin/PurBeurreWebApp).

# In production, for adding [Sentry](https://sentry.io), a cron job to update and backup the database:

### Create pur_beurre_django_app/settings/production.py :
```python
# settings for a production environment
from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://<key>@sentry.io/111111",
    integrations=[DjangoIntegration()]
)

SECRET_KEY = 'New secret key'
DEBUG = False
ALLOWED_HOSTS = ['IP.SE.RV.ER']

DATABASES = {
    # New Database configuration
}

# Use mailjet to send confirmation email
EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'
MAILJET_API_KEY = 'API_KEY'
MAILJET_API_SECRET = 'API_SECRET'
DEFAULT_FROM_EMAIL = "PurBeurre <example@example.com>"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use Dropbox for the backup
# attention for Password see https://github.com/pajadam/django-dbbackup/commit/a5d167df3466d055844b908c9a0103ec02fce606
DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': '<token>',
}
```
### Create the cron job (every monday at 7:00am)
```bash
$ crontab -e
```
```
0 7 * * mon /home/username/TestTravisCI/cronjob.sh
```
