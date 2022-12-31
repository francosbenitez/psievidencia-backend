import unidecode
from apps.psychologists.models import GenderPerspective


def seed_gender_perspective(df):
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
