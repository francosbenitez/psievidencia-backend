from django.shortcuts import render
from django.core.paginator import Paginator 

from .models import Psychologist

def index(request):
    psychologists = Psychologist.objects.all()
    psychologist_paginator = Paginator(psychologists, 10)
    page_num = request.GET.get('page')
    page = psychologist_paginator.get_page(page_num)
    context = {
        'count' : psychologist_paginator.count,
        'page' : page
    }
    return render(request, 'psychologists/index.html', context)
