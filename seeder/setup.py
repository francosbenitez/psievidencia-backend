def setup_django(root_path, settings):
    import os
    import django
    import sys

    os.chdir(root_path)

    print("os.chdir", os.chdir)

    # Django settings
    sys.path.append(root_path)

    print("sys.path", sys.path)

    os.environ["DJANGO_SETTINGS_MODULE"] = settings

    django.setup()
