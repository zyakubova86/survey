import json
import mimetypes
import os
from datetime import timedelta
from pprint import pprint

import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Count, ExpressionWrapper, IntegerField, FloatField, F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .models import *
from django.core.serializers.json import DjangoJSONEncoder

import datetime


def home(request):
    if "/ru/" in request.path:
        template = 'mainapp/home_ru.html'
    else:
        template = 'mainapp/home_uz.html'

    return render(request, template)



def submit_survey(request):
    if "/ru/" in request.path:
        template = 'mainapp/survey_ru.html'
    else:
        template = 'mainapp/survey_uz.html'

    questions = Question.objects.filter(is_active=True).prefetch_related('options').order_by('order')
    departments = Department.objects.filter(is_active=True, name_uz__isnull=False, name_ru__isnull=False).exclude(name_uz='', name_ru='').order_by('name_uz')

    context = {
        'questions': questions,
        'departments': departments,
    }

    return render(request, template, context)
