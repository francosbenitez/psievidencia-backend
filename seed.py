import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import csv
from apps.psychologists.models import Psychologist

req = requests.get(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQngt5TxTabbOavo5qHaZz5ohs9o_46sWrhQMKT5gJdedIG3Icq0qvuUX1dfdkcrmqNUxzCjOk2egSo/pub?gid=160193944&single=true&output=csv"
)
url_content = req.content
csv_file = open("psychologists.csv", "wb")

csv_file.write(url_content)
csv_file.close()

CSV_PATH = "./psychologists.csv"

contSuccess = 0
Psychologist.objects.all().delete()

with open(CSV_PATH, newline="") as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    next(reader)
    print("Loading...")
    for i, row in enumerate(reader):
        print("row", row)
        Psychologist.objects.create(
            id=i,
            date=row[0],
            name=row[1],
            email=row[2],
            gender=row[3],
            registration_type=row[4],
            registration_number=row[5],
            institution=row[6],
            team=row[7],
            province=row[8],
            city=row[9],
            education=row[10],
            therapeutic_model=row[11],
            gender_perspective=row[12],
            specialization=row[13],
            work_population=row[14],
            work_modality=row[15],
            online=row[16],
            prepaid=row[17],
            prepaid_type=row[18],
            invoice=row[19],
            sign_language=row[20],
            session_languages=row[21],
            social_networks=row[22],
            phone_number=row[23],
            additional_data=row[24],
            name_2=row[25],
        )
        contSuccess += 1
    print(f"{str(contSuccess)} inserted successfully! ")
