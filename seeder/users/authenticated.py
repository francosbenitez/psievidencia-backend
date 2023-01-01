from apps.users.models import User, Authenticated


def seed_authenticated():
    print("Seeding authenticated user...")

    if not User.objects.filter(email__iexact="username@email.com").exists():
        user = Authenticated.objects.create_user(
            username="username",
            email="username@email.com",
            password="password",
            is_email_verified=True,
            role="AUTHENTICATED",
        )
        user.save()

        print("User seeded!")
