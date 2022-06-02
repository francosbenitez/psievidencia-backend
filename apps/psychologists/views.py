from django.shortcuts import render
from django.core.paginator import Paginator 

from .models import Psychologist
from .serializers import PsychologistSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class PaginatedPsychologists(APIView):
  def get(self, request, format=None):
    psychologists = Psychologist.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(psychologists, request)
    serializer = PsychologistSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

class LatestPsychologistsList(APIView):
  def get(self, request, format=None):
    psychologists = Psychologist.objects.all()[0:4]
    serializer = PsychologistSerializer(psychologists, many=True)
    return Response(serializer.data)
