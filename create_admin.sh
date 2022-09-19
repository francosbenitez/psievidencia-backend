echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@email.com', 'admin')" | python manage.py shell
