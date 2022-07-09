from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
import pandas as pd
from .models import (
    Psychologist,
    Specialization,
    TherapeuticModel,
    WorkPopulation,
    Education,
)
from .serializers import (
    PsychologistSerializer,
    SpecializationSerializer,
    TherapeuticModelSerializer,
    WorkPopulationSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.db import connection


class PaginatedPsychologists(APIView):
    def get(self, request, format=None):
        psychologists = Psychologist.objects.all().order_by("id")
        specializations = Specialization.objects.all()
        name = None
        education = None
        specialization = None
        work_population = None
        therapeutic_model = None

        def dictfetchall(cursor):
            "Returns all rows from a cursor as a dict"
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
            ]

        if "name" in request.GET:
            name = request.GET["name"]

        if "education" in request.GET:
            education = request.GET["education"]

        if "specialization[]" in request.GET:
            specialization = list(map(int, request.GET.getlist("specialization[]")))

        if "therapeutic_model[]" in request.GET:
            therapeutic_model = list(
                map(int, request.GET.getlist("therapeutic_model[]"))
            )

        if "work_population[]" in request.GET:
            work_population = list(map(int, request.GET.getlist("work_population[]")))

        if name or education or specialization or work_population or therapeutic_model:
            if name is not None:
                psychologists = psychologists.filter(name__icontains=name)

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

            if specialization is not None:
                cursor = connection.cursor()
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."id") "psychologists_psychologist"."id", "psychologists_psychologist"."name", "psychologists_psychologist"."therapeutic_model",  "psychologists_psychologist"."specialization", "psychologists_psychologist"."work_population" FROM "psychologists_psychologist" INNER JOIN "psychologists_specialization_psychologists" ON ("psychologists_psychologist"."id" = "psychologists_specialization_psychologists"."psychologist_id") WHERE "psychologists_specialization_psychologists"."specialization_id" IN {} GROUP BY "psychologists_psychologist"."id" HAVING COUNT(*) = {}'

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
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."id") "psychologists_psychologist"."id", "psychologists_psychologist"."name", "psychologists_psychologist"."therapeutic_model",  "psychologists_psychologist"."specialization", "psychologists_psychologist"."work_population" FROM "psychologists_psychologist" INNER JOIN "psychologists_therapeuticmodel_psychologists" ON ("psychologists_psychologist"."id" = "psychologists_therapeuticmodel_psychologists"."psychologist_id") WHERE "psychologists_therapeuticmodel_psychologists"."therapeuticmodel_id" IN {} GROUP BY "psychologists_psychologist"."id" HAVING COUNT(*) = {}'

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
                query = 'SELECT DISTINCT ON ("psychologists_psychologist"."id") "psychologists_psychologist"."id", "psychologists_psychologist"."name", "psychologists_psychologist"."work_population",  "psychologists_psychologist"."specialization", "psychologists_psychologist"."work_population" FROM "psychologists_psychologist" INNER JOIN "psychologists_workpopulation_psychologists" ON ("psychologists_psychologist"."id" = "psychologists_workpopulation_psychologists"."psychologist_id") WHERE "psychologists_workpopulation_psychologists"."workpopulation_id" IN {} GROUP BY "psychologists_psychologist"."id" HAVING COUNT(*) = {}'

                work_population_len = len(work_population)
                work_population_tuple = tuple(work_population)

                if work_population_len == 1:
                    work_population_tuple = "(%s)" % ", ".join(
                        map(repr, work_population_tuple)
                    )

                query = query.format(work_population_tuple, work_population_len)

                cursor.execute(query)
                psychologists = psychologists.filter(id__in=(x[0] for x in cursor))

        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(psychologists, request)
        serializer = PsychologistSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PsychologistDetail(APIView):
    def get_object(self, psychologist_id):
        try:
            return Psychologist.objects.get(id=psychologist_id)
        except Psychologist.DoesNotExist:
            raise Http404

    def get(self, request, psychologist_id, format=None):
        psychologist = self.get_object(psychologist_id)
        serializer = PsychologistSerializer(psychologist)
        return Response(serializer.data)


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
