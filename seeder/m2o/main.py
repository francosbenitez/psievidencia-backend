from .utils.education import seed_education
from .utils.gender_identity import seed_gender_identity
from .utils.gender_perspective import seed_gender_perspective
from .utils.prepaid import seed_prepaid
from .utils.province import seed_province


def seed_m2o(df):
    seed_education(df)
    seed_gender_identity(df)
    seed_gender_perspective(df)
    seed_prepaid(df)
    seed_province(df)
