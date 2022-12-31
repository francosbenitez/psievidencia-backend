import unidecode
from datetime import datetime, date
import secrets
import pandas as pd
from apps.psychologists.models import Psychologist
from apps.users.models import User
from utils.constants import DATA_DICT


def seed_psychologists(reader):
    print("Seeding psychologists...")

    data_to_join = pd.DataFrame.from_dict(DATA_DICT)

    for i, row in enumerate(reader):

        if row[2] != "":
            if row[25] != "":
                if row[1] == "":
                    row[1] = row[25]
                row[1] = unidecode.unidecode(row[1]).lower().title()

            if row[0] == "":
                format = "%d/%m/%Y %H:%M:%S"
                today = date.today()
                inctime = today.strftime("%d/%m/%Y %H:%M:%S")
                time = datetime.strptime(inctime, format)
                time.strftime("%Y/%m/%d %H:%M:%S")
                row[0] = time
            else:
                format = "%d/%m/%Y %H:%M:%S"
                inctime = row[0]
                time = datetime.strptime(inctime, format)
                time.strftime("%Y/%m/%d %H:%M:%S")
                row[0] = time

            if (
                not Psychologist.objects.filter(id=i).exists()
                and not User.objects.filter(email=row[2]).exists()
            ):
                data_to_join = data_to_join.append(
                    {
                        "therapeutic_model": row[11],
                        "specialization": row[13],
                        "work_population": row[14],
                        "work_modality": row[15],
                        "province": row[8],
                        "gender_identity": row[3],
                        "gender_perspective": row[12],
                        "prepaid": row[17],
                        "education": row[10],
                    },
                    ignore_index=True,
                )

                password_length = 8
                random_password = secrets.token_urlsafe(password_length)

                Psychologist.objects.create_user(
                    date=row[0],
                    name=row[1],
                    email=row[2],
                    username=row[2].split("@")[0],
                    password=random_password,
                    is_email_verified=True,
                    role="PSYCHOLOGIST",
                    registration_type=row[4],
                    registration_number=row[5],
                    institution=row[6],
                    team=row[7],
                    city=row[9],
                    online=row[16],
                    prepaid_type=row[18],
                    invoice=row[19],
                    sign_language=row[20],
                    session_languages=row[21],
                    social_networks=row[22],
                    phone_number=row[23],
                    additional_data=row[24],
                    name_2=row[25],
                )

    return data_to_join

    print("Psychologists seeded!")
