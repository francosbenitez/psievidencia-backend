import unidecode
from datetime import datetime, date
import secrets
import pandas as pd
from apps.psychologists.models import Psychologist
from apps.users.models import User
from utils.constants import DATA_DICT


def seed_psychologists(reader):
    print("Seeding psychologists...")

    relationships = pd.DataFrame.from_dict(DATA_DICT)

    for i, row in enumerate(reader):
        date_csv = row[0]
        name = row[1]
        email = row[2]
        gender_identity = row[3]
        registration_type = row[4]
        registration_number = row[5]
        institution = row[6]
        team = row[7]
        province = row[8]
        city = row[9]
        education = row[10]
        therapeutic_model = row[11]
        gender_perspective = row[12]
        specialization = row[13]
        work_population = row[14]
        work_modality = row[15]
        online = row[16]
        prepaid = row[17]
        prepaid_type = row[18]
        invoice = row[19]
        sign_language = row[20]
        session_languages = row[21]
        social_networks = row[22]
        phone_number = row[23]
        additional_data = row[24]
        name_2 = row[25]

        password_length = 8
        random_password = secrets.token_urlsafe(password_length)
        username = email.split("@")[0]
        password = random_password
        is_email_verified = True
        role = "PSYCHOLOGIST"

        if email != "":
            if name_2 != "":
                if name == "":
                    name = name_2
                name = unidecode.unidecode(name).lower().title()

            if date_csv == "":
                format = "%d/%m/%Y %H:%M:%S"
                today = date.today()
                inctime = today.strftime("%d/%m/%Y %H:%M:%S")
                time = datetime.strptime(inctime, format)
                time.strftime("%Y/%m/%d %H:%M:%S")
                date_csv = time
            else:
                format = "%d/%m/%Y %H:%M:%S"
                inctime = date_csv
                time = datetime.strptime(inctime, format)
                time.strftime("%Y/%m/%d %H:%M:%S")
                date_csv = time

            if not User.objects.filter(email__iexact=email).exists():

                psy_rel = pd.DataFrame(
                    [
                        {
                            "therapeutic_model": therapeutic_model,
                            "specialization": specialization,
                            "work_population": work_population,
                            "work_modality": work_modality,
                            "province": province,
                            "gender_identity": gender_identity,
                            "gender_perspective": gender_perspective,
                            "prepaid": prepaid,
                            "education": education,
                        }
                    ]
                )

                relationships = pd.concat([relationships, psy_rel], ignore_index=True)

                Psychologist.objects.create_user(
                    date=date_csv,
                    name=name,
                    email=email,
                    username=username,
                    password=password,
                    is_email_verified=is_email_verified,
                    role=role,
                    registration_type=registration_type,
                    registration_number=registration_number,
                    institution=institution,
                    team=team,
                    city=city,
                    online=online,
                    prepaid_type=prepaid_type,
                    invoice=invoice,
                    sign_language=sign_language,
                    session_languages=session_languages,
                    social_networks=social_networks,
                    phone_number=phone_number,
                    additional_data=additional_data,
                    name_2=name_2,
                )

    print("Psychologists seeded!")

    return relationships
