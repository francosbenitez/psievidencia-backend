from apps.users.models import Authenticated


def seed_authenticated():
    print("Seeding authenticated user...")

    if not Authenticated.objects.filter(username="username").exists():
        user = Authenticated.objects.create_user(
            username="username",
            email="username@email.com",
            password="password",
            is_email_verified=True,
            role="AUTHENTICATED",
        )
        user.save()

        print("User seeded!")
