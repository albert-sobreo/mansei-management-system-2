from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime
import re
from .journalAPI import jeAPI
from .petty_cash_api import *

class BIR2307View(View):
    def get(self, request):
        return render(request, '2307.html')

class BIR0619EView(View):
    def get(self, request):
        return render(request, '0619-E.html')