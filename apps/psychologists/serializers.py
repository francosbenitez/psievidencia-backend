from rest_framework import serializers
from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    WorkModality,
    Province,
    Education,
    Prepaid,
    GenderPerspective,
    GenderIdentity,
)


class TherapeuticModelSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        data = super(TherapeuticModelSerializer, self).to_representation(value)

        views = ["PaginatedPsychologists", "PsychologistDetail", "FavoritesList"]

        if "view" in self.context:
            if self.context["view"] in views:
                return value.name

        return data

    class Meta:
        model = TherapeuticModel
        fields = ("id", "name")


class SpecializationSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        data = super(SpecializationSerializer, self).to_representation(value)

        views = ["PaginatedPsychologists", "PsychologistDetail", "FavoritesList"]

        if "view" in self.context:
            if self.context["view"] in views:
                return value.name

        return data

    class Meta:
        model = Specialization
        fields = ("id", "name")


class WorkModalitySerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        data = super(WorkModalitySerializer, self).to_representation(value)

        views = ["PaginatedPsychologists", "PsychologistDetail", "FavoritesList"]

        if "view" in self.context:
            if self.context["view"] in views:
                return value.name

        return data

    class Meta:
        model = WorkModality
        fields = ("id", "name")


class WorkPopulationSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        data = super(WorkPopulationSerializer, self).to_representation(value)

        views = ["PaginatedPsychologists", "PsychologistDetail", "FavoritesList"]

        if "view" in self.context:
            if self.context["view"] in views:
                return value.name

        return data

    class Meta:
        model = WorkPopulation
        fields = ("id", "name")


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("id", "name", "slug")


class PsychologistsSerializer(serializers.ModelSerializer):
    therapeutic_models = TherapeuticModelSerializer(many=True)
    specializations = SpecializationSerializer(many=True)
    work_populations = WorkPopulationSerializer(many=True)
    work_modalities = WorkModalitySerializer(many=True)
    province = serializers.SerializerMethodField()

    class Meta:
        model = Psychologist
        fields = (
            "id",
            "name",
            "email",
            "province",
            "therapeutic_models",
            "specializations",
            "work_populations",
            "work_modalities",
            "liked",
        )

    def get_province(self, obj):
        list = []
        provinces = obj.province.all()
        for province in provinces:
            list.append(province.slug)
        return " ".join(list)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ("id", "name")


class PrepaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepaid
        fields = ("id", "has_prepaid")


class GenderIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenderIdentity
        fields = ("id", "gender_identity")


class GenderPerspectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenderPerspective
        fields = ("id", "has_perspective")


class PsychologistSerializer(PsychologistsSerializer):
    liked = serializers.SerializerMethodField()
    gender_identity = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    gender_perspective = serializers.SerializerMethodField()
    prepaid = serializers.SerializerMethodField()

    class Meta(PsychologistsSerializer.Meta):
        fields = PsychologistsSerializer.Meta.fields + (
            "date",
            "gender_identity",
            "registration_type",
            "registration_number",
            "institution",
            "team",
            "city",
            "education",
            "gender_perspective",
            "online",
            "prepaid",
            "prepaid_type",
            "invoice",
            "sign_language",
            "session_languages",
            "social_networks",
            "phone_number",
            "additional_data",
            "name_2",
            "username",
        )

    def get_liked(self, obj):
        if "liked" in self.context:
            liked = self.context["liked"]
            return liked
        return

    def get_gender_identity(self, obj):

        d = {"no_binarie": "No binarie", "varon": "Hombre", "mujer": "Mujer"}

        list = []
        gender_identities = obj.gender_identity.all()

        for gender_identity in gender_identities:
            list.append(d[gender_identity.gender_identity])

        return " ".join(list)

    def get_education(self, obj):

        d = {
            "licenciatura": "Licenciatura",
            "especialidad": "Especialidad",
            "maestria": "Maestría",
            "doctorado": "Doctorado",
        }

        list = []
        educations = obj.education.all()

        for education in educations:
            list.append(d[education.name])

        return " ".join(list)

    def get_gender_perspective(self, obj):

        d = {"si": "Sí", "no": "No"}

        list = []
        gender_perspectives = obj.gender_perspective.all()

        for gender_perspective in gender_perspectives:
            list.append(d[gender_perspective.has_perspective])

        return " ".join(list)

    def get_prepaid(self, obj):

        d = {"si": "Sí", "no": "No"}

        list = []
        prepaids = obj.prepaid.all()

        for prepaid in prepaids:
            list.append(d[prepaid.has_prepaid])

        return " ".join(list)


class RegisterPsychologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Psychologist
        fields = (
            "id",
            "email",
            "username",
            "password",
            "name",
            "province",
            "gender_identity",
            "registration_type",
            "registration_number",
            "institution",
            "team",
            "city",
            "education",
            "gender_perspective",
            "online",
            "prepaid",
            "prepaid_type",
            "invoice",
            "sign_language",
            "session_languages",
            "social_networks",
            "phone_number",
            "additional_data",
        )

    def get_fields(self):
        fields = super(RegisterPsychologistSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
            field.allow_blank = False
        return fields

    def create(self, validated_data):
        return Psychologist.objects.create_user(**validated_data)
