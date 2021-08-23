from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from decimal import Decimal
from datetime import datetime

class BankReconView(View):
    def get(self, request, format=None):
        return render(request, 'bank-recon.html')