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
from datetime import datetime
from datetime import date

class PaymentVoucherView(View):
    def get(self, request, format=None):
        
        try:
            pv = request.user.branch.paymentVoucher.latest('pk')

            listed_code = pv.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'PV-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'PV-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'PV-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'po': request.user.branch.purchaseOrder.filter(approved=True, fullyPaid=False)
        }

        return render(request, 'payment-voucher.html', context)

class SavePaymentVoucher(APIView):
    def post(self, request, format = None):
        paymentVoucher = request.data

        pv = PaymentVoucher()
        pv.code = paymentVoucher['code']
        pv.datetimeCreated = datetime.now()
        pv.remarks = paymentVoucher['description']
        if paymentVoucher['retroactive']:
            pv.paymentDate = paymentVoucher['retroactive']
        else:
            pv.paymentDate = paymentVoucher['date']
        if request.user.is_authenticated:
            pv.createdBy = request.user
        pv.paymentMethod = paymentVoucher['paymentMethod']
        pv.amountPaid = paymentVoucher['amountPaid']
        pv.wep = paymentVoucher['wep']
        pv.purchaseOrder = PurchaseOrder.objects.get(pk=paymentVoucher['po']['code'])
        pv.save()
        request.user.branch.paymentVoucher.add(pv)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SalesInvoiceView(View):
    def get(self, request, format=None):

        try:
            si = request.user.branch.salesInvoice.latest('pk')

            listed_code = si.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'SI-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'SI-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            listed_date = str(now.today()).split('-')
            new_code = 'SI-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
            'sc': request.user.branch.salesContract.filter(approved=True, fullyPaid=False)
        }

        return render(request, 'sales-invoice.html', context)

class SaveSalesInvoice(APIView):
    def post(self, request, format = None):
        salesInvoice = request.data

        si = SalesInvoice()
        si.code = salesInvoice['code']
        si.datetimeCreated = datetime.now()
        si.remarks = salesInvoice['description']
        if salesInvoice['retroactive']:
            si.paymentDate = salesInvoice['retroactive']
        else:
            si.paymentDate = salesInvoice['date']
        if request.user.is_authenticated:
            si.createdBy = request.user
        si.paymentMethod = salesInvoice['paymentMethod']
        si.amountPaid = salesInvoice['amountPaid']
        si.wep = salesInvoice['wep']
        si.salesContract = SalesContract.objects.get(pk=salesInvoice['sc']['code'])
        si.save()
        request.user.branch.salesInvoice.add(si)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
