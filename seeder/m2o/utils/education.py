import unidecode
from apps.psychologists.models import Education


def seed_education(df):
    print("Seeding education...")
    education_df = df[["id", "education"]].copy(deep=True)

    education_df["education"] = education_df["education"].apply(
        lambda row: unidecode.unidecode(row).lower()
    )

    for row in education_df.itertuples():
        if not Education.objects.filter(id=row[0]).exists():
            Education.objects.create(
                id=row[0],
                psychologists_id=row[1],
                name=row[2],
            )
    print("Education seeded!")
