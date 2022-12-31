def setup_django(root_path, settings):
    import os
    import django
    import sys

    os.chdir(root_path)
    sys.path.append(root_path)
    os.environ["DJANGO_SETTINGS_MODULE"] = settings
    django.setup()
