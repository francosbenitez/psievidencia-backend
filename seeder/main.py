import pandas as pd
import csv
from utils.utils import update_csv
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
    Psychologist.objects.all().delete()

    seed_authenticated()

    with open(CSV_PATH, newline="") as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        next(reader)

        data_to_join = seed_psychologists(reader)
        df = pd.DataFrame(list(Psychologist.objects.all().values()))
        df = df.join(data_to_join)

        seed_m2m(df)
        seed_m2o(df)

        print("Seeder was applied successfully!")


if __name__ == "__main__":
    update_csv()
    seed_all()
