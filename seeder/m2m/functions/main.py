def seed(new_df, column_name, model):
    print(f"Seeding {column_name.replace('_', ' ')}...")

    new_df.columns = new_df.columns.str.replace("id", "psychologist_id")
    new_df["id"] = new_df.index + 1

    new_df[column_name] = new_df[column_name].apply(
        lambda row: row.strip() if row is not None else row
    )

    new_df_options = new_df[column_name].value_counts().index.tolist()

    for i, item in enumerate(new_df_options, start=1):
        if not model.objects.filter(id=i).exists() and item != "":
            model.objects.create(
                id=i,
                name=item,
            )

    for row in new_df.itertuples():
        for option in model.objects.all().values():
            if row[2] == option["name"]:
                model.objects.get(pk=option["id"]).psychologists.add(row[1])

    print(f"{column_name.replace('_', ' ')} seeded!")
