import unidecode
from apps.psychologists.models import Prepaid


def seed_prepaid(df):
    print("Seeding prepaid...")
    prepaid_df = df[["id", "prepaid"]].copy(deep=True)

    prepaid_df["prepaid"] = prepaid_df["prepaid"].apply(
        lambda row: unidecode.unidecode(row).lower()
    )

    for row in prepaid_df.itertuples():
        if not Prepaid.objects.filter(id=row[0]).exists():
            Prepaid.objects.create(
                id=row[0],
                psychologists_id=row[1],
                has_prepaid=row[2],
            )
    print("Prepaid seeded!")
