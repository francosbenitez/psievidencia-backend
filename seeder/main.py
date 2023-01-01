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

        relationships = seed_psychologists(reader)
        relationships.to_excel("seeder/data/relationships.xlsx")

        psychologists = pd.DataFrame(list(Psychologist.objects.all().values()))

        psy_rel = psychologists.join(relationships)
        psy_rel["date"] = psy_rel["date"].dt.tz_localize(None)
        psy_rel["date_joined"] = psy_rel["date_joined"].dt.tz_localize(None)
        psy_rel.to_excel("seeder/data/psy_rel.xlsx")

        seed_m2m(psy_rel)
        seed_m2o(psy_rel)

        print("Seeder was applied successfully!")


if __name__ == "__main__":
    update_csv()
    seed_all()
