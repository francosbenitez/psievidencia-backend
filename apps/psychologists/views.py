from django.shortcuts import render
from django.core.paginator import Paginator 
from django.http import Http404

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
