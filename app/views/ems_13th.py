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
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class EMS_13thMonthView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        context = {
            'users': request.user.branch.user.exclude(authLevel='dtr')
        }

        return render(request, 'ems-13th.html', context)