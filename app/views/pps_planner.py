from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime, date
import re

class PPS_ProjectPlannerView(View):
    def get(self, request):
        return render(request, 'pps-planner.html')