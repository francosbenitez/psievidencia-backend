from django.http import Http404
from apps.users.models import Authenticated
from apps.users.serializers import AuthenticatedSerializer
from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkModality,
    WorkPopulation,
    Province,
)
from .serializers import (
    PsychologistSerializer,
    PsychologistsSerializer,
    SpecializationSerializer,
    TherapeuticModelSerializer,
    WorkPopulationSerializer,
    ProvinceSerializer,
)
from apps.favorites.models import Favorite
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from rest_framework import generics, status

# from .paginations import CustomPagination


class PaginatedPsychologists(APIView):
    # pagination_class = CustomPagination

    def get(self, request, format=None):
        psychologists = Psychologist.objects.all().order_by("-id")
        
        name = None
        education = None
        has_perspective = None
        has_prepaid = None
        specialization = None
        work_population = None
        therapeutic_model = None
        gender_identity = None
        work_modality = None
        province = None

        if "name" in request.GET:
            name = request.GET["name"]

        if "education" in request.GET:
            education = request.GET["education"]

        if "has_perspective" in request.GET:
            has_perspective = request.GET["has_perspective"]

        if "has_prepaid" in request.GET:
            has_prepaid = request.GET["has_prepaid"]

        if "gender_identity" in request.GET:
            gender_identity = request.GET["gender_identity"]

        if "province" in request.GET:
            province = request.GET["province"]

        if "specialization[]" in request.GET:
            specialization = list(map(int, request.GET.getlist("specialization[]")))

        if "therapeutic_model[]" in request.GET:
            therapeutic_model = list(
                map(int, request.GET.getlist("therapeutic_model[]"))
            )

        if "work_population[]" in request.GET:
            work_population = list(map(int, request.GET.getlist("work_population[]")))

        if "work_modality[]" in request.GET:
            work_modality = list(map(int, request.GET.getlist("work_modality[]")))

        if (
            name
            or education
            or has_perspective
            or has_prepaid
            or gender_identity
            or specialization
            or work_population
            or therapeutic_model
            or work_modality
            or province
        ):
            if name is not None:
                psychologists = psychologists.filter(name__icontains=name)

            if province is not None:
                psychologists = psychologists.filter(
                    provinces__name__icontains=province
                )

            if education is not None:
                if (
                    education == "licenciatura"
                    or education == "maestria"
                    or education == "doctorado"
                    or education == "especialidad"
                ):
                    psychologists = psychologists.filter(
                        educations__name__icontains=education
                    )

            if has_perspective is not None:
                if has_perspective == "si" or has_perspective == "no":
                    psychologists = psychologists.filter(
                        gender_perspectives__has_perspective__icontains=has_perspective
                    )

            if has_prepaid is not None:
                if has_prepaid == "si" or has_prepaid == "no":
                    psychologists = psychologists.filter(
                        prepaids__has_prepaid__icontains=has_prepaid
                    )

            if gender_identity is not None:
                if (
                    gender_identity == "varon"
                    or gender_identity == "mujer"
                    or gender_identity == "no_binarie"
                ):
                    psychologists = psychologists.filter(
                        gender_identities__gender_identity__icontains=gender_identity
                    )

            if specialization is not None:
                cursor = connection.cursor()
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."user_ptr_id") "psychologists_psychologist"."user_ptr_id" FROM "psychologists_psychologist" INNER JOIN "psychologists_specialization_psychologists" ON ("psychologists_psychologist"."user_ptr_id" = "psychologists_specialization_psychologists"."psychologist_id") WHERE "psychologists_specialization_psychologists"."specialization_id" IN {} GROUP BY "psychologists_psychologist"."user_ptr_id" HAVING COUNT(*) = {}'

                specialization_len = len(specialization)
                specialization_tuple = tuple(specialization)

                if specialization_len == 1:
                    specialization_tuple = "(%s)" % ", ".join(
                        map(repr, specialization_tuple)
                    )

                query = query.format(specialization_tuple, specialization_len)

                cursor.execute(query)
                psychologists = psychologists.filter(id__in=(x[0] for x in cursor))

            if therapeutic_model is not None:
                cursor = connection.cursor()
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."user_ptr_id") "psychologists_psychologist"."user_ptr_id" FROM "psychologists_psychologist" INNER JOIN "psychologists_therapeuticmodel_psychologists" ON ("psychologists_psychologist"."user_ptr_id" = "psychologists_therapeuticmodel_psychologists"."psychologist_id") WHERE "psychologists_therapeuticmodel_psychologists"."therapeuticmodel_id" IN {} GROUP BY "psychologists_psychologist"."user_ptr_id" HAVING COUNT(*) = {}'

                therapeutic_model_len = len(therapeutic_model)
                therapeutic_model_tuple = tuple(therapeutic_model)

                if therapeutic_model_len == 1:
                    therapeutic_model_tuple = "(%s)" % ", ".join(
                        map(repr, therapeutic_model_tuple)
                    )

                query = query.format(therapeutic_model_tuple, therapeutic_model_len)

                cursor.execute(query)
                psychologists = psychologists.filter(id__in=(x[0] for x in cursor))

            if work_population is not None:
                cursor = connection.cursor()
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."user_ptr_id") "psychologists_psychologist"."user_ptr_id" FROM "psychologists_psychologist" INNER JOIN "psychologists_workpopulation_psychologists" ON ("psychologists_psychologist"."user_ptr_id" = "psychologists_workpopulation_psychologists"."psychologist_id") WHERE "psychologists_workpopulation_psychologists"."workpopulation_id" IN {} GROUP BY "psychologists_psychologist"."user_ptr_id" HAVING COUNT(*) = {}'

                work_population_len = len(work_population)
                work_population_tuple = tuple(work_population)

                if work_population_len == 1:
                    work_population_tuple = "(%s)" % ", ".join(
                        map(repr, work_population_tuple)
                    )

                query = query.format(work_population_tuple, work_population_len)

                cursor.execute(query)
                psychologists = psychologists.filter(id__in=(x[0] for x in cursor))

            if work_modality is not None:
                cursor = connection.cursor()
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."user_ptr_id") "psychologists_psychologist"."user_ptr_id" FROM "psychologists_psychologist" INNER JOIN "psychologists_workmodality_psychologists" ON ("psychologists_psychologist"."user_ptr_id" = "psychologists_workmodality_psychologists"."psychologist_id") WHERE "psychologists_workmodality_psychologists"."workmodality_id" IN {} GROUP BY "psychologists_psychologist"."user_ptr_id" HAVING COUNT(*) = {}'

                work_modality_len = len(work_modality)
                work_modality_tuple = tuple(work_modality)

                if work_modality_len == 1:
                    work_modality_tuple = "(%s)" % ", ".join(
                        map(repr, work_modality_tuple)
                    )

                query = query.format(work_modality_tuple, work_modality_len)

                cursor.execute(query)
                psychologists = psychologists.filter(id__in=(x[0] for x in cursor))

        list_psychologists = list(psychologists.values())

        custom_list = [item["id"] for item in list_psychologists]
        queryset = Psychologist.objects.filter(id__in=custom_list).order_by("-id")

        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PsychologistsSerializer(
            result_page, context={"view": "PaginatedPsychologists"}, many=True
        )

        user_id = request.user.id
        if user_id:

            favorites = Favorite.objects.filter(authenticated_id=user_id)

            favorites_psychologists = []

            for item in favorites.values():
                try:
                    favorite = psychologists.filter(id=item["psychologist_id"]).values()
                    favorites_psychologists.append(favorite[0])
                except IndexError:
                    pass

            for item_fa in favorites_psychologists:
                for item_ps in serializer.data:
                    if item_fa["id"] == item_ps["id"]:
                        item_ps["liked"] = True

        return paginator.get_paginated_response(serializer.data)


class PsychologistDetail(APIView):
    def get_object(self, psychologist_id):
        try:
            return Psychologist.objects.filter(id=psychologist_id).values()[0]
        except Psychologist.DoesNotExist:
            raise Http404

    def get(self, request, psychologist_id, format=None):
        psychologist = self.get_object(psychologist_id)

        user_id = request.user.id

        if user_id:

            favorites = Favorite.objects.filter(authenticated_id=user_id)
            favorites_psychologists = []

            for item in favorites.values():
                try:
                    favorite = Psychologist.objects.filter(
                        id=item["psychologist_id"]
                    ).values()
                    favorites_psychologists.append(favorite[0])
                except IndexError:
                    pass

            for item_fa in favorites_psychologists:
                if item_fa == psychologist:
                    psychologist["liked"] = True

        queryset = Psychologist.objects.get(id=psychologist["id"])

        serializer = PsychologistSerializer(
            queryset,
            context={"liked": psychologist["liked"], "view": "PsychologistDetail"},
        )

        return Response(serializer.data)


class UpdatePsychologist(generics.GenericAPIView):
    def patch(self, request, format=None):
        user_id = request.user.id
        user_role = request.user.role

        if user_id:
            if user_role == "PSYCHOLOGIST":
                psychologist = Psychologist.objects.get(id=user_id)

                data_to_change = request.data

                def update_many_to_many(string, model, relationship):
                    if request.data.get(string) != None:
                        array = []

                        for item in request.data.get(string):
                            model_object = model.objects.get(id=item["id"])
                            array.append(model_object)

                        relationship.set(array)
                        del data_to_change[string]

                arr_of_dicts = [
                    {
                        "string": "therapeutic_models",
                        "model": TherapeuticModel,
                        "relation": psychologist.therapeutic_models,
                    },
                    {
                        "string": "work_modalities",
                        "model": WorkModality,
                        "relation": psychologist.work_modalities,
                    },
                    {
                        "string": "work_populations",
                        "model": WorkPopulation,
                        "relation": psychologist.work_populations,
                    }
                ]

                for dict in arr_of_dicts:
                    update_many_to_many(dict["string"], dict["model"], dict["relation"])

                Psychologist.objects.filter(id=user_id).update(**data_to_change)
                
                psychologist = Psychologist.objects.get(id=user_id)
                serializer = PsychologistSerializer(
                    psychologist, context={"liked": psychologist.liked}
                )

                return Response(
                    {"message": "success", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                authenticated = Authenticated.objects.get(id=user_id)
                data_to_change = request.data
                Authenticated.objects.filter(id=user_id).update(**data_to_change)
                authenticated = Authenticated.objects.get(id=user_id)
                serializer = AuthenticatedSerializer(authenticated)

                return Response(
                    {"message": "success", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )

        return Response(
            {"message": "error"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SpecializationsList(APIView):
    def get(self, request, format=None):
        specializations = Specialization.objects.all().order_by("id")
        name = None

        if "name" in request.GET:
            name = request.GET["name"]

        if name:
            if name is not None:
                specializations = specializations.filter(name__icontains=name)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(specializations, request)
        serializer = SpecializationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TherapeuticModelsList(APIView):
    def get(self, request, format=None):
        therapeutic_models = TherapeuticModel.objects.all().order_by("id")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(therapeutic_models, request)
        serializer = TherapeuticModelSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class WorkPopulationsList(APIView):
    def get(self, request, format=None):
        work_populations = WorkPopulation.objects.all().order_by("id")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(work_populations, request)
        serializer = WorkPopulationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProvincesList(APIView):
    def get(self, request, format=None):
        provinces = Province.objects.all().order_by("id")
        provinces_values = Province.objects.values()
        provinces_list = [entry for entry in provinces_values]

        # Removes provinces list duplicates
        found = set()
        remove_provinces_list_duplicates = []
        for dct in provinces_list:
            if dct["name"] not in found:
                remove_provinces_list_duplicates.append(dct)
                found.add(dct["name"])

        # Creates a list of dictionaries to be sent as a JSON
        json = []
        for i, item in enumerate(remove_provinces_list_duplicates):
            dic = {}
            dic["id"] = i
            dic["name"] = item["name"]
            dic["slug"] = item["slug"]
            json.append(dic)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(json, request)
        serializer = ProvinceSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
