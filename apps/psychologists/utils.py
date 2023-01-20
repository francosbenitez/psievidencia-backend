from rest_framework import serializers


def validate_profile(profile):
    strings_to_check = ["https", ":", "//", "www", "instagram", ".com", "/"]

    for string in strings_to_check:
        if string in profile:
            raise serializers.ValidationError(
                "Por favor, ingresá el nombre de usuario."
            )

    return profile
