from .utils.specialization import seed_specialization
from .utils.therapeutic_model import seed_therapeutic_model
from .utils.work_population import seed_work_population


def seed_m2m(df):
    seed_specialization(df)
    seed_therapeutic_model(df)
    seed_work_population(df)
