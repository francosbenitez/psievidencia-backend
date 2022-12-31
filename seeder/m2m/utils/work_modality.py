from m2m.functions.main import seed
from apps.psychologists.models import WorkModality


def seed_work_modality(df):
    work_modality_df = (
        df[["id", "work_modality"]]
        .assign(work_modality=df["work_modality"].str.split(","))
        .explode("work_modality")
        .reset_index(drop=True)
    )

    seed(work_modality_df, "work_modality", WorkModality)
