from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
import pandas as pd
from .models import Psychologist, Specialization
from .serializers import PsychologistSerializer, SpecializationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view


class PaginatedPsychologists(APIView):
    def get(self, request, format=None):
        psychologists = Psychologist.objects.all().order_by("id")
        paginator = PageNumberPagination()
        paginator.page_size = 10
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
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def search(request, format=None):
    psychologists = Psychologist.objects.order_by("id")
    specializations = Specialization.objects.all()

    name = None
    specialization = None
    work_population = None
    therapeutic_model = None

    if "name" in request.GET:
        name = request.GET["name"]

    if "specialization[]" in request.GET:
        specialization = list(map(int, request.GET.getlist("specialization[]")))

    if "work_population" in request.GET:
        work_population = request.GET["work_population"]

    if "therapeutic_model" in request.GET:
        therapeutic_model = request.GET["therapeutic_model"]

    if name or specialization or work_population or therapeutic_model:
        if name is not None:
            psychologists = psychologists.filter(name__icontains=name)

        if specialization is not None:
            print("specialization", specialization)
            psychologists = psychologists.filter(specializations__id__in=specialization)

        if work_population is not None:
            psychologists = psychologists.filter(
                work_population__icontains=work_population
            )

        if therapeutic_model is not None:
            psychologists = psychologists.filter(
                therapeutic_model__icontains=therapeutic_model
            )

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(psychologists, request)
        serializer = PsychologistSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({"psychologists": []})
