import os
import django
import requests
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import csv
from apps.psychologists.models import Psychologist, Specialization, TherapeuticModel

req = requests.get(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQngt5TxTabbOavo5qHaZz5ohs9o_46sWrhQMKT5gJdedIG3Icq0qvuUX1dfdkcrmqNUxzCjOk2egSo/pub?gid=160193944&single=true&output=csv"
)
url_content = req.content
csv_file = open("psychologists.csv", "wb")

csv_file.write(url_content)
csv_file.close()

CSV_PATH = "./psychologists.csv"

Psychologist.objects.all().delete()

with open(CSV_PATH, newline="") as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    next(reader)

    # Seed psychologists
    for i, row in enumerate(reader):
        Psychologist.objects.create(
            id=i + 1,
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

    # Build df
    df = pd.DataFrame(list(Psychologist.objects.all().values()))

    # Seed 'specialization'
    df_specialization = (
        df[["id", "specialization"]]
        .assign(specialization=df["specialization"].str.split(","))
        .explode("specialization")
        .reset_index(drop=True)
    )
    df_specialization.columns = df_specialization.columns.str.replace(
        "id", "psychologist_id"
    )
    df_specialization["id"] = df_specialization.index + 1

    df_specialization["specialization"] = df_specialization["specialization"].apply(
        lambda row: row.strip() if row is not None else row
    )

    specialization_options = (
        df_specialization["specialization"].value_counts().index.tolist()
    )

    for i, item in enumerate(specialization_options, start=1):
        Specialization.objects.create(
            id=i,
            specialization=item,
        )

    for row in df_specialization.itertuples():
        for specialization_option in Specialization.objects.all().values():
            if row[2] == specialization_option["specialization"]:
                Specialization.objects.get(
                    pk=specialization_option["id"]
                ).psychologists.add(row[1])
