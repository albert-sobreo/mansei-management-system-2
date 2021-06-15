import json
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from django.http.response import Http404
import pandas as pd

class ImportATC(View):
    def post(self, request, format=None):
        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))

        for jsonATC in jsonDF:
            atc = ATC()

            if ATC.objects.filter(code=jsonATC['code'], rate=jsonATC['rate'], description=jsonATC['description']):
                print(jsonATC['code'] + ' exists')
                continue
            atc.code = jsonATC['code']
            atc.rate = jsonATC['rate']
            atc.description = jsonATC['description']
            atc.save()
        
        sweetify.sweetalert(request, icon="success", title="Success!", persistent="Dismiss")
        return redirect('/purchase-order/')