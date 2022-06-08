import pandas as pd
from django.core.management.base import BaseCommand
from apps.psychologists.models import Psychologist
from sqlalchemy import create_engine
from django.conf import settings


class Command(BaseCommand):
    help = "A command to add data from an CSV file to the database"

    def handle(self, *args, **options):
        csv_file = "psychologists.csv"
        df = pd.read_csv(csv_file)
        df.columns = [
            "date",
            "name",
            "email",
            "gender",
            "registration_type",
            "registration_number",
            "institution",
            "team",
            "province",
            "city",
            "education",
            "therapeutic_model",
            "gender_perspective",
            "specialization",
            "work_population",
            "work_modality",
            "online",
            "prepaid",
            "prepaid_type",
            "invoice",
            "sign_language",
            "session_languages",
            "social_networks",
            "phone_number",
            "additional_data",
            "name_2",
        ]
        df["id"] = df.index + 1
        column_to_move = df.pop("id")
        df.insert(0, "id", column_to_move)
        user = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        database_name = settings.DATABASES["default"]["NAME"]
        database_url = (
            "postgresql://{user}:{password}@localhost:5432/{database_name}".format(
                user=user,
                password=password,
                database_name=database_name,
            )
        )
        engine = create_engine(database_url, echo=False)
        df.to_sql(
            Psychologist._meta.db_table, if_exists="replace", con=engine, index=False
        )
