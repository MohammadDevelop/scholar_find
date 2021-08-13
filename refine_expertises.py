import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','schfind.settings')
django.setup()
from schrest.models import Expertise
from django.utils import timezone

all_expertises = Expertise.objects.all()
print(len(all_expertises))

for exp in all_expertises:
    if len(exp.title) < 4 :
        print(exp.title +" Deleted !")
        exp.delete()