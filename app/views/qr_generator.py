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
from ..models import*
from .notificationCreate import *

class QRGeneratorView(View):
    def get(self, request):
        return render(request, 'qr-generator.html')