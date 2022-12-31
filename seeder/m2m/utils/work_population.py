from m2m.functions.main import seed
from apps.psychologists.models import WorkPopulation


def seed_work_population(df):
    work_population_df = (
        df[["id", "work_population"]]
        .assign(work_population=df["work_population"].str.split(","))
        .explode("work_population")
        .reset_index(drop=True)
    )

    seed(work_population_df, "work_population", WorkPopulation)
