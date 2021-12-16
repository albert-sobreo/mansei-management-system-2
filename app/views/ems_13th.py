from rest_framework.views import APIView
from ..models import *
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
import datetime
from .journalAPI import jeAPI
import io
import xlsxwriter
import string

class EMS_13thMonthView(View):
    def get(self, request):
        context = {
            'users': request.user.branch.user.exclude(authLevel='dtr')
        }

        return render(request, 'ems-13th.html', context)