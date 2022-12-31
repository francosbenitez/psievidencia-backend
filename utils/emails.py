import sys
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from pandas import DataFrame

sys.path.insert(0, "")

from seeder.setup import setup_django

PROJECT_PATH = "./"
PROJECT_SETTING = "config.settings"

setup_django(PROJECT_PATH, PROJECT_SETTING)

from apps.psychologists.models import Psychologist

psychologists = Psychologist.objects.order_by("id")


def send_bulk():
    emails_successful = []
    emails_failed = []
    for (i, psychologist) in enumerate(psychologists):
        try:
            msg_html = render_to_string(
                "hello.html",
                {"name": psychologist.name},
            )

            send_mail(
                f"¡Hola, {psychologist.name}! Nos encantaría tu feedback",
                "",
                settings.EMAIL_HOST_USER,
                [psychologist.email],
                html_message=msg_html,
                fail_silently=False,
            )
            email_successful = psychologist.email
            print(f"The message has been sent successfully.")
            print(f"Email succesful: {email_successful}")
            emails_successful.append(email_successful)

            emails_failed.append(None)

        except:
            email_failed = psychologist.email
            print(f"It has been an error.")
            print(f"Psychologist email: {email_failed}")
            emails_failed.append(email_failed)

            emails_successful.append(None)

    return emails_successful, emails_failed


def write_file(se, fe):
    df = DataFrame({"Succesful Emails": se, "Failed Emails": fe})
    df.to_excel("emails.xlsx", sheet_name="sheet1", index=False)
    print("Written!")


if __name__ == "__main__":
    es, ef = send_bulk()
    write_file(es, ef)
