from rest_framework.views import APIView
from ..models import MerchandiseInventory, Warehouse, WarehouseItems
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime, date

class ReturnYearsView(View):
    def get(self, request):
        yearNow = date.today().year
        yearList = [i for i in range(yearNow+1, 1999, -1)]
        
        return JsonResponse(yearList, safe=False)