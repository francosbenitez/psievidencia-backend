import pandas as pd
from django.core.management.base import BaseCommand
from apps.psychologists.models import Psychologist


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.DataFrame(list(Psychologist.objects.all().values()))

        new_df = (
            df[["specialization", "id"]]
            .assign(specialization=df["specialization"].str.split(","))
            .explode("specialization")
            .reset_index(drop=True)
        )

        print("new_df", new_df)

        specialization_options = (
            new_df["specialization"].value_counts().index.tolist(),
        )
        # TO-DO: 1) Make an API with the following structure:
        # When people select the filter by specialization -let's say by "Sexología"-, it must appear the set of psychologists ("id") who have an specialization in "Sexología".
        # API: /api/psychologists?specialization[]=1
        # where "1" is the ID of the specialization.j
        # The result will be the set of psychologists who has that specialization.

        # /api/psychologists?type=specialization
        # This returns a JSON with all the specialization fields:
        # {
        #   "specialization": "Primeros Auxilios Psicológicos",
        #   "id": 1
        # }