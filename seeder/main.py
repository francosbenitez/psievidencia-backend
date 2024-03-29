import os
import django
import pandas as pd
import unidecode
from datetime import datetime, date
from utils import update_csv
import secrets
from setup import setup_django

PROJECT_PATH = "./"
PROJECT_SETTING = "config.settings"

setup_django(PROJECT_PATH, PROJECT_SETTING)

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

from apps.users.models import Authenticated, User


def main_seeder():
    CSV_PATH = "./seeder/psychologists.csv"

    Psychologist.objects.all().delete()

    # Seed user
    print("Seeding authenticated user...")
    if Authenticated.objects.filter(username="username").exists():
        pass
    else:
        user = Authenticated.objects.create_user(
            username="username",
            email="username@email.com",
            password="password",
            is_email_verified=True,
            role="AUTHENTICATED",
        )
        user.save()
    print("User seeded!")

    with open(CSV_PATH, newline="") as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        next(reader)

        df_test = pd.DataFrame.from_dict(
            {
                "therapeutic_model": [],
                "specialization": [],
                "work_population": [],
                "work_population": [],
                "province": [],
                "gender_identity": [],
                "gender_perspective": [],
                "prepaid": [],
                "education": [],
            }
        )

        # Seed psychologists
        print("Seeding psychologists...")
        for i, row in enumerate(reader):

            if row[2] != "":
                if row[25] != "":
                    if row[1] == "":
                        row[1] = row[25]
                    row[1] = unidecode.unidecode(row[1]).lower().title()

                if row[0] == "":
                    format = "%d/%m/%Y %H:%M:%S"
                    today = date.today()
                    inctime = today.strftime("%d/%m/%Y %H:%M:%S")
                    time = datetime.strptime(inctime, format)
                    time.strftime("%Y/%m/%d %H:%M:%S")
                    row[0] = time
                else:
                    format = "%d/%m/%Y %H:%M:%S"
                    inctime = row[0]
                    time = datetime.strptime(inctime, format)
                    time.strftime("%Y/%m/%d %H:%M:%S")
                    row[0] = time

                if (
                    not Psychologist.objects.filter(id=i).exists()
                    and not User.objects.filter(email=row[2]).exists()
                ):
                    df_test = df_test.append(
                        {
                            "therapeutic_model": row[11],
                            "specialization": row[13],
                            "work_population": row[14],
                            "work_modality": row[15],
                            "province": row[8],
                            "gender_identity": row[3],
                            "gender_perspective": row[12],
                            "prepaid": row[17],
                            "education": row[10],
                        },
                        ignore_index=True,
                    )

                    password_length = 8
                    random_password = secrets.token_urlsafe(password_length)

                    Psychologist.objects.create_user(
                        date=row[0],
                        name=row[1],
                        email=row[2],
                        username=row[2].split("@")[0],
                        password=random_password,
                        is_email_verified=True,
                        role="PSYCHOLOGIST",
                        registration_type=row[4],
                        registration_number=row[5],
                        institution=row[6],
                        team=row[7],
                        city=row[9],
                        online=row[16],
                        prepaid_type=row[18],
                        invoice=row[19],
                        sign_language=row[20],
                        session_languages=row[21],
                        social_networks=row[22],
                        phone_number=row[23],
                        additional_data=row[24],
                        name_2=row[25],
                    )
        print("Psychologists seeded!")

        # Build df
        df = pd.DataFrame(list(Psychologist.objects.all().values()))
        df = df.join(df_test)

        # Create seed function to seed 'specialization', 'therapeutic_model', 'work_population' & 'work_modality'
        def seed(new_df, column_name, model):
            print(f"Seeding {column_name.replace('_', ' ')}...")
            new_df.columns = new_df.columns.str.replace("id", "psychologist_id")
            new_df["id"] = new_df.index + 1

            new_df[column_name] = new_df[column_name].apply(
                lambda row: row.strip() if row is not None else row
            )

            new_df_options = new_df[column_name].value_counts().index.tolist()

            for i, item in enumerate(new_df_options, start=1):
                if not model.objects.filter(id=i).exists() and item != "":
                    model.objects.create(
                        id=i,
                        name=item,
                    )

            for row in new_df.itertuples():
                for option in model.objects.all().values():
                    if row[2] == option["name"]:
                        model.objects.get(pk=option["id"]).psychologists.add(row[1])
            print(f"{column_name.replace('_', ' ')} seeded!")

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
        print("Seeding education...")
        education_df = df[["id", "education"]].copy(deep=True)

        education_df["education"] = education_df["education"].apply(
            lambda row: unidecode.unidecode(row).lower()
        )

        for row in education_df.itertuples():
            if not Education.objects.filter(id=row[0]).exists():
                Education.objects.create(
                    id=row[0],
                    psychologists_id=row[1],
                    name=row[2],
                )
        print("Education seeded!")

        # Seed 'province'
        print("Seeding province...")
        province_df = df[["id", "province"]].copy(deep=True)

        province_df["slug"] = province_df["province"]

        province_df["province"] = (
            province_df["province"]
            .apply(lambda row: unidecode.unidecode(row).lower())
            .apply(lambda row: row.replace("buenos aires capital federal", "caba"))
            .apply(lambda row: row.replace("buenos aires provincia", "gba"))
            .apply(lambda row: row.replace("santiago del estero", "santiago"))
            .apply(lambda row: row.replace(" ", "_"))
        )

        for row in province_df.itertuples():
            if not Province.objects.filter(id=row[0]).exists():
                if row[2] != "":
                    Province.objects.create(
                        id=row[0], psychologists_id=row[1], name=row[2], slug=row[3]
                    )
        print("Province seeded!")

        # Seed 'gender_perspective'
        print("Seeding gender perspective...")
        gender_perspective_df = df[["id", "gender_perspective"]].copy(deep=True)

        gender_perspective_df["gender_perspective"] = gender_perspective_df[
            "gender_perspective"
        ].apply(lambda row: unidecode.unidecode(row).lower())

        for row in gender_perspective_df.itertuples():
            if not GenderPerspective.objects.filter(id=row[0]).exists():
                GenderPerspective.objects.create(
                    id=row[0],
                    psychologists_id=row[1],
                    has_perspective=row[2],
                )
        print("Gender perspective seeded!")

        # Seed 'prepaid'
        print("Seeding prepaid...")
        prepaid_df = df[["id", "prepaid"]].copy(deep=True)

        prepaid_df["prepaid"] = prepaid_df["prepaid"].apply(
            lambda row: unidecode.unidecode(row).lower()
        )

        for row in prepaid_df.itertuples():
            if not Prepaid.objects.filter(id=row[0]).exists():
                Prepaid.objects.create(
                    id=row[0],
                    psychologists_id=row[1],
                    has_prepaid=row[2],
                )
        print("Prepaid seeded!")

        # Seed 'gender_identity'
        print("Seeding gender identity..")
        gender_identity_df = df[["id", "gender_identity"]].copy(deep=True)

        gender_identity_df["gender_identity"] = (
            gender_identity_df["gender_identity"]
            .apply(lambda row: unidecode.unidecode(row).lower())
            .apply(lambda row: row.replace(" ", "_"))
        )

        for row in gender_identity_df.itertuples():
            if not GenderIdentity.objects.filter(id=row[0]).exists():
                GenderIdentity.objects.create(
                    id=row[0],
                    psychologists_id=row[1],
                    gender_identity=row[2],
                )
        print("Gender identity seeded!")
        print("Seeder was applied successfully!")


if __name__ == "__main__":
    update_csv()
    main_seeder()
