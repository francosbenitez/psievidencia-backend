import unidecode
from apps.psychologists.models import Province


def seed_province(df):
    print("Seeding province...")
    province_df = df[["id", "province"]].copy(deep=True)

    province_df["slug"] = province_df["province"]

    province_df["province"] = (
        province_df["province"]
        .apply(lambda row: unidecode.unidecode(row).lower())
        .apply(lambda row: row.replace("buenos aires capital federal", "caba"))
        .apply(lambda row: row.replace("buenos aires provincia", "gba"))
        .apply(lambda row: row.replace("santiago del estero", "santiago"))
        .apply(lambda row: row.replace(" ", "_"))
    )

    for row in province_df.itertuples():
        if not Province.objects.filter(id=row[0]).exists():
            if row[2] != "":
                Province.objects.create(
                    psychologists_id=row[1], name=row[2], slug=row[3]
                )
    print("Province seeded!")
