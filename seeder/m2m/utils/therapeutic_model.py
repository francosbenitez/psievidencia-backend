from m2m.helpers.main import seed
from apps.psychologists.models import TherapeuticModel


def seed_therapeutic_model(df):
    therapeutic_model_df = (
        df[["id", "therapeutic_model"]]
        .assign(therapeutic_model=df["therapeutic_model"].str.split(","))
        .explode("therapeutic_model")
        .reset_index(drop=True)
    )

    seed(therapeutic_model_df, "therapeutic_model", TherapeuticModel)
