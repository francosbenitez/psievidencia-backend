import os
import django
import requests
import pandas as pd
import unidecode

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
    GenderIdentity,
    WorkModality,
    Province,
)

# from django.contrib.auth.models import User
from apps.users.models import User

req = requests.get(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQngt5TxTabbOavo5qHaZz5ohs9o_46sWrhQMKT5gJdedIG3Icq0qvuUX1dfdkcrmqNUxzCjOk2egSo/pub?gid=160193944&single=true&output=csv"
)
url_content = req.content
csv_file = open("psychologists.csv", "wb")

csv_file.write(url_content)
csv_file.close()

CSV_PATH = "./psychologists.csv"

Psychologist.objects.all().delete()

# Seed user
user = User.objects.create_user(
    username="username",
    email="username@email.com",
    password="password",
    is_email_verified=True,
)
user.save()

with open(CSV_PATH, newline="") as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    next(reader)

    # Seed psychologists
    for i, row in enumerate(reader):
        if row[25] != "":
            if row[1] == "":
                row[1] = row[25]
            row[1] = unidecode.unidecode(row[1]).lower().title()

            Psychologist.objects.create(
                id=i + 1,
                date=row[0],
                name=row[1],
                email=row[2],
                gender_identity=row[3],
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

    # Create seed function to seed 'specialization', 'therapeutic_model' & 'work_population'
    def seed(new_df, column_name, model):
        new_df.columns = new_df.columns.str.replace("id", "psychologist_id")
        new_df["id"] = new_df.index + 1

        new_df[column_name] = new_df[column_name].apply(
            lambda row: row.strip() if row is not None else row
        )

        new_df_options = new_df[column_name].value_counts().index.tolist()

        for i, item in enumerate(new_df_options, start=1):
            model.objects.create(
                id=i,
                name=item,
            )

        for row in new_df.itertuples():
            for option in model.objects.all().values():
                if row[2] == option["name"]:
                    model.objects.get(pk=option["id"]).psychologists.add(row[1])

    # Seed 'specialization'
    specialization_df = (
        df[["id", "specialization"]]
        .assign(specialization=df["specialization"].str.split(","))
        .explode("specialization")
        .reset_index(drop=True)
    )

    seed(specialization_df, "specialization", Specialization)

    # Seed 'therapeutic_model'
    therapeutic_model_df = (
        df[["id", "therapeutic_model"]]
        .assign(therapeutic_model=df["therapeutic_model"].str.split(","))
        .explode("therapeutic_model")
        .reset_index(drop=True)
    )

    seed(therapeutic_model_df, "therapeutic_model", TherapeuticModel)

    # Seed 'work_population'
    work_population_df = (
        df[["id", "work_population"]]
        .assign(work_population=df["work_population"].str.split(","))
        .explode("work_population")
        .reset_index(drop=True)
    )

    seed(work_population_df, "work_population", WorkPopulation)

    # Seed 'work_modality'
    work_modality_df = (
        df[["id", "work_modality"]]
        .assign(work_modality=df["work_modality"].str.split(","))
        .explode("work_modality")
        .reset_index(drop=True)
    )

    seed(work_modality_df, "work_modality", WorkModality)

    # Seed 'education'
    education_df = df[["id", "education"]].copy(deep=True)

    education_df["education"] = education_df["education"].apply(
        lambda row: unidecode.unidecode(row).lower()
    )

    for row in education_df.itertuples():
        Education.objects.create(
            id=row[0],
            psychologists_id=row[1],
            name=row[2],
        )

    # Seed 'province'
    province_df = df[["id", "province"]].copy(deep=True)

    province_df["province"] = (
        province_df["province"]
        .apply(lambda row: unidecode.unidecode(row).lower())
        .apply(lambda row: row.replace("buenos aires capital federal", "caba"))
        .apply(lambda row: row.replace("buenos aires provincia", "gba"))
        .apply(lambda row: row.replace("santiago del estero", "santiago"))
        .apply(lambda row: row.replace(" ", "_"))
    )

    for row in province_df.itertuples():
        Province.objects.create(
            id=row[0],
            psychologists_id=row[1],
            name=row[2],
        )

    # Seed 'gender_perspective'
    gender_perspective_df = df[["id", "gender_perspective"]].copy(deep=True)

    gender_perspective_df["gender_perspective"] = gender_perspective_df[
        "gender_perspective"
    ].apply(lambda row: unidecode.unidecode(row).lower())

    for row in gender_perspective_df.itertuples():
        GenderPerspective.objects.create(
            id=row[0],
            psychologists_id=row[1],
            has_perspective=row[2],
        )

    # Seed 'gender_identity'
    gender_identity_df = df[["id", "gender_identity"]].copy(deep=True)

    gender_identity_df["gender_identity"] = (
        gender_identity_df["gender_identity"]
        .apply(lambda row: unidecode.unidecode(row).lower())
        .apply(lambda row: row.replace(" ", "_"))
    )

    for row in gender_identity_df.itertuples():
        GenderIdentity.objects.create(
            id=row[0],
            psychologists_id=row[1],
            gender_identity=row[2],
        )
