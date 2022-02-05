from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from decimal import Decimal
from datetime import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class HTMLtoEXCELView(View):
    def get(self, request):
        return render(request, 'html-to-excel.html')