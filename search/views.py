from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import datetime
from search.models import Vegetable, Record


# Create your views here.

def today(request):
    vegtables = Record.objects.filter(created_at__day=datetime.date.today().day)
    vegtables = [v.as_dict() for v in vegtables]

    return JsonResponse(vegtables, safe=False)
