import os
import django
import pandas as pd
import unidecode
from datetime import datetime, date
from utils import update_csv
import secrets

# from django.template.loader import render_to_string
# from django.core.mail import send_mail
# from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import csv
from apps.psychologists.models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    Education,
    GenderPerspective,
    Prepaid,
    GenderIdentity,
    WorkModality,
    Province,
)

from apps.users.models import Authenticated


def main_seeder():
    CSV_PATH = "./seeder/psychologists.csv"

    print("Psychologist.objects.all()", Psychologist.objects.all())
    print("CSV_PATH", CSV_PATH)


if __name__ == "__main__":
    update_csv()
    main_seeder()
