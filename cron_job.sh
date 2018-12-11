# use the virtual environment for python
source /home/jbthepenguin/Documents/formation/projets/10_mise_ligne_nutella/codeGitHub/TestTravisCI/env/bin/activate
# update the database
python /home/jbthepenguin/Documents/formation/projets/10_mise_ligne_nutella/codeGitHub/TestTravisCI/manage.py update_db --settings=pur_beurre_django_app.settings.production
# backup the database
python /home/jbthepenguin/Documents/formation/projets/10_mise_ligne_nutella/codeGitHub/TestTravisCI/manage.py dbbackup --settings=pur_beurre_django_app.settings.production
