import unidecode
from apps.psychologists.models import GenderIdentity


def seed_gender_identity(df):
    print("Seeding gender identity..")
    gender_identity_df = df[["id", "gender_identity"]].copy(deep=True)

    gender_identity_df["gender_identity"] = (
        gender_identity_df["gender_identity"]
        .apply(lambda row: unidecode.unidecode(row).lower())
        .apply(lambda row: row.replace(" ", "_"))
    )

    for row in gender_identity_df.itertuples():
        if not GenderIdentity.objects.filter(id=row[0]).exists():
            GenderIdentity.objects.create(
                id=row[0],
                psychologists_id=row[1],
                gender_identity=row[2],
            )
    print("Gender identity seeded!")
