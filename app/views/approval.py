from rest_framework.views import APIView
from ..models import *
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
import sweetify
from decimal import Decimal
from datetime import datetime

################# PURCHASE REQUEST #################
class PRapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'purchase': user.branch.purchaseRequest.filter(approved=True),
        }
        return render(request, 'pr-approved.html', context)

class PRnonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'purchase': user.branch.purchaseRequest.filter(approved=False),
        }
        return render(request, 'pr-nonapproved.html', context)

class PRApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        prequest = PurchaseRequest.objects.get(pk=pk)

        prequest.datetimeApproved = datetime.now()
        prequest.approved = True
        prequest.approvedBy = request.user
        prequest.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
        
        
        
        
        
        
        
        
        
################# PURCHASE ORDER #################

class POapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'purchase': user.branch.purchaseOrder.filter(approved=True),
        }
        return render(request, 'po-approved.html', context)

class POnonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'purchase': user.branch.purchaseOrder.filter(approved=False),
        }
        return render(request, 'po-nonapproved.html', context)

class POApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        purchase = PurchaseOrder.objects.get(pk=pk)

        purchase.datetimeApproved = datetime.now()
        purchase.approved = True
        purchase.approvedBy = request.user
        

        purchase.save()

        j = Journal()

        j.code = purchase.code
        j.datetimeCreated = purchase.datetimeApproved
        j.createdBy = purchase.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        

        je = JournalEntries()
        wep = JournalEntries()
        wep.journal = j
        wep.normally = 'Credit'
        wep.accountChild = AccountChild.objects.get(name="Withholding Expanded Payables")
        # wep.amount = purchase.poatc.amountWithheld
        for poatc in purchase.poatc.all():
            wep.amount = poatc.amountWithheld
        wep.accountChild.amount = wep.amount
        wep.accountChild.accountSubGroup.amount -= wep.amount
        wep.accountChild.accountSubGroup.accountGroup.amount -= wep.amount
        wep.accountChild.save()
        wep.accountChild.accountSubGroup.save()
        wep.accountChild.accountSubGroup.accountGroup.save()
        wep.balance = wep.accountChild.amount
        wep.save()
        request.user.branch.journalEntries.add(wep)
        vat = JournalEntries()
        vat.journal = j
        vat.normally = 'Credit'
        vat.accountChild = AccountChild.objects.get(name="VAT Amount")
        vat.amount = purchase.taxPeso
        vat.accountChild.accountSubGroup.amount -= vat.amount
        vat.accountChild.accountSubGroup.accountGroup.amount -= vat.amount
        vat.accountChild.save()
        vat.accountChild.accountSubGroup.save()
        vat.accountChild.accountSubGroup.accountGroup.save()
        vat.balance = vat.accountChild.amount
        vat.save()
        request.user.branch.journalEntries.add(vat)
        

        if purchase.paymentPeriod == 'Full Payment':
            if purchase.paymentMethod == 'Cash on Hand':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.accountSubGroup.amount -= je.amount
                je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                je.accountChild.save()
                je.accountChild.accountSubGroup.save()
                je.accountChild.accountSubGroup.accountGroup.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journalEntries.add(je)
            elif purchase.paymentMethod == 'Cash in Bank':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.accountSubGroup.amount -= je.amount
                je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                je.accountChild.save()
                je.accountChild.accountSubGroup.save()
                je.accountChild.accountSubGroup.accountGroup.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journalEntries.add(je)
        elif purchase.paymentPeriod == 'Partial Payment':
            if purchase.paymentMethod == 'Cash on Hand':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.accountSubGroup.amount -= je.amount
                je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                je.accountChild.save()
                je.accountChild.accountSubGroup.save()
                je.accountChild.accountSubGroup.accountGroup.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journalEntries.add(je)

                payables = JournalEntries()

                payables.journal = j
                payables.normally = "Credit"
                payables.accountChild = purchase.party.accountChild.get(name="Trade Payables - " + purchase.party.name)
                payables.amount = purchase.amountTotal - purchase.amountPaid
                payables.accountChild.amount += je.amount
                payables.accountChild.accountSubGroup.amount += je.amount
                payables.accountChild.accountSubGroup.accountGroup.amount += je.amount
                payables.accountChild.save()
                payables.accountChild.accountSubGroup.save()
                payables.accountChild.accountSubGroup.accountGroup.save()
                payables.balance = je.accountChild.amount
                payables.save()
                request.user.branch.journalEntries.add(payables)

            elif purchase.paymentMethod == 'Cash in Bank':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.accountSubGroup.amount -= je.amount
                je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                je.accountChild.save()
                je.accountChild.accountSubGroup.save()
                je.accountChild.accountSubGroup.accountGroup.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journalEntries.add(je)

                payables = JournalEntries()

                payables.journal = j
                payables.normally = "Credit"
                payables.accountChild = purchase.party.accountChild.get(name="Trade Payables - " + purchase.party.name)
                payables.amount = purchase.amountTotal - purchase.amountPaid
                payables.accountChild.amount += je.amount
                payables.accountChild.accountSubGroup.amount += je.amount
                payables.accountChild.accountSubGroup.accountGroup.amount += je.amount
                payables.accountChild.save()
                payables.accountChild.accountSubGroup.save()
                payables.accountChild.accountSubGroup.accountGroup.save()
                payables.balance = je.accountChild.amount
                payables.save()
                request.user.branch.journalEntries.add(payables)
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)









########## RECEIVING REPORT ##########
class RRnonapproved(View):
    def get(self, request, format=None):
        context = {
            'purchase': request.user.branch.receivingReport.filter(approved=False),
        }
        return render(request, 'rr-nonapproved.html', context)

class RRapproved(View):
    def get(self, request, format=None):
        context = {
            'purchase': request.user.branch.receivingReport.filter(approved=True)
        }
        return render(request, 'rr-approved.html', context)

class RRApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        receive = ReceivingReport.objects.get(pk=pk)

        receive.datetimeApproved = datetime.now()
        receive.approved = True
        receive.approvedBy = request.user
        
        for element in receive.rritemsmerch.all():
            element.merchInventory.qtyA += element.qty
            element.merchInventory.qtyT = element.merchInventory.qtyA + element.merchInventory.qtyR
            element.merchInventory.totalCost += element.totalPrice                
            element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
            element.merchInventory.save()

        receive.save()

        j = Journal()

        j.code = receive.code
        j.datetimeCreated = receive.datetimeApproved
        j.createdBy = receive.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        je = JournalEntries()

        je.journal = j
        je.normally = 'Debit'
        je.accountChild = AccountChild.objects.get(name='Merchandise Inventory')
        je.amount = receive.amountDue
        je.accountChild.amount += je.amount
        je.accountChild.accountSubGroup.amount += je.amount
        je.accountChild.accountSubGroup.accountGroup.amount += je.amount
        je.accountChild.save()
        je.accountChild.accountSubGroup.save()
        je.accountChild.accountSubGroup.accountGroup.save()
        je.balance = je.accountChild.amount
        je.save()
        request.user.branch.journalEntries.add(je)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)






################# SALES #################

class SCapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'sales': user.branch.salesContract.filter(approved=True),
        }
        return render(request, 'sc-approved.html', context)

class SCnonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'sales': user.branch.salesContract.filter(approved=False),
        }
        return render(request, 'sc-nonapproved.html', context)

class SCApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        sale = TempSalesContract.objects.get(pk=pk)

        sale.datetimeApproved = datetime.now()
        sale.approved = True
        sale.approvedBy = request.user
        
        for element in sale.tempscitemsmerch.all():
            element.merchInventory.qtyA -= element.qty
            element.merchInventory.qtyT = element.merchInventory.qtyA - element.merchInventory.qtyR
            element.merchInventory.totalCost += element.totalCost                
            # element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
            element.merchInventory.save()

        sale.save()

        j = Journal()

        j.code = sale.code
        j.datetimeCreated = sale.datetimeApproved
        j.createdBy = sale.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        je = JournalEntries()

        je.journal = j
        je.normally = 'Credit'
        je.accountChild = AccountChild.objects.get(name='Merchandise Inventory')
        je.amount = sale.totalCost
        je.accountChild.amount -= je.amount
        je.accountChild.save()
        je.balance = je.accountChild.amount
        je.save()
        request.user.branch.journalEntries.add(je)

        je = JournalEntries()

        je.journal = j
        je.normally = 'Debit'
        je.accountChild = AccountChild.objects.get(name="Cash on Hand")
        je.amount = sale.totalCost
        je.accountChild.amount += je.amount
        je.accountChild.save()
        je.balance = je.accountChild.amount
        je.save()
        request.user.branch.journalEntries.add(je)

        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)




        

################# DELIVERIES #################
class DeliveriesNonApproved(View):
    def get(self, request, format=None):
        context = {
            'deliveries': request.user.branch.deliveries.filter(approved=False)
        }
        return render(request, 'deliveriesnonapproved.html', context)

class DeliveriesApproved(View):
    def get(self, request, format=None):
        context = {
            'deliveries': request.user.branch.deliveries.filter(approved=True)
        }
        return render(request, 'deliveriesapproved.html', context)

class DeliveriesApprovalAPI(APIView):
    def put(self, request, pk, format = None):
        deliveries = request.data
        d = Deliveries.objects.get(pk=pk)


        d.datetimeApproved = datetime.now()
        d.approved = True
        d.truck.status = 'In-transit'
        d.truck.driver = d.driver
        d.driver.status = 'In-transit'
        d.truck.currentDelivery = d.pk
        d.truck.save()
        d.driver.save()
        d.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)