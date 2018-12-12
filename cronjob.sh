#!/bin/bash

# use the virtual environment for python
source /home/purbeurre/TestTravisCI/env/bin/activate
# update the database
python /home/purbeurre/TestTravisCI/manage.py update_db --settings=pur_beurre_django_app.settings.production
# backup the database
python /home/purbeurre/TestTravisCI/manage.py dbbackup --settings=pur_beurre_django_app.settings.production
