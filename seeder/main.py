import pandas as pd
import csv
from utils.helpers import update_csv
from utils.setup import setup_django
from utils.constants import PROJECT_PATH, PROJECT_SETTING, CSV_PATH

setup_django(PROJECT_PATH, PROJECT_SETTING)

from apps.psychologists.models import (
    Psychologist,
)

from users.authenticated import seed_authenticated
from users.psychologists import seed_psychologists
from m2m.main import seed_m2m
from m2o.main import seed_m2o


def seed_all():
    seed_authenticated()

    with open(CSV_PATH, newline="") as csvfile:
        reader = csv.reader(csvfile, quotechar='"')

        next(reader)

        # if there are new psychologists, 'relationships' returns only those
        relationships, flag, flag_email = seed_psychologists(reader)
        relationships.to_excel("seeder/data/relationships.xlsx")

        # before, there is no problem. The problem is, from here, below ->
        print("flag_email", flag_email)
        psychologists = pd.DataFrame(
            list(Psychologist.objects.filter(email__in=flag_email).values())
        )

        psy_rel = psychologists.join(relationships)

        psy_rel["date"] = psy_rel["date"].dt.tz_localize(None)
        psy_rel["date_joined"] = psy_rel["date_joined"].dt.tz_localize(None)
        psy_rel.to_excel("seeder/data/psy_rel.xlsx")

        psy_rel = psy_rel.dropna(
            subset=[
                "therapeutic_model",
                "specialization",
                "work_population",
                "work_population",
                "province",
                "gender_identity",
                "gender_perspective",
                "prepaid",
                "education",
            ]
        )

        print("psy_rel", psy_rel)

        if flag:
            seed_m2m(psy_rel)
            seed_m2o(psy_rel)

        print("Seeder was applied successfully!")


if __name__ == "__main__":
    update_csv()
    seed_all()
