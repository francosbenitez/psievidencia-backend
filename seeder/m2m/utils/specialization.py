from m2m.functions.main import seed
from apps.psychologists.models import Specialization


def seed_specialization(df):
    specialization_df = (
        df[["id", "specialization"]]
        .assign(specialization=df["specialization"].str.split(","))
        .explode("specialization")
        .reset_index(drop=True)
    )

    seed(specialization_df, "specialization", Specialization)
