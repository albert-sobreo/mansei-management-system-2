from django import views
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
from decimal import Decimal

class PaymentVoucherView(View):
    def get(self, request, format=None):
        return render(request, 'payment-voucher.html')

class SalesInvoiceView(View):
    def get(self, request, format=None):
        return render(request, 'sales-invoice.html')
