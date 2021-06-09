from rest_framework.views import APIView
from app.models import PurchaseOrder, Journal, JournalEntries, AccountChild
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

        purchase.datetimeApproved = request.data['datetimeApproved']
        purchase.approved = True
        purchase.approvedBy = request.user
        
        for element in purchase.poitemsmerch.all():
            element.merchInventory.qtyA += element.qty
            element.merchInventory.qtyT = element.merchInventory.qtyA + element.merchInventory.qtyR
            element.merchInventory.totalCost += element.totalPrice                
            element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
            element.merchInventory.save()

        purchase.save()

        j = Journal()

        j.code = purchase.code
        j.datetimeCreated = purchase.datetimeApproved
        j.createdBy = purchase.createdBy
        j.journalDate = purchase.datetimeApproved
        j.save()
        request.user.branch.journal.add(j)

        je = JournalEntries()

        je.journal = j
        je.normally = 'Debit'
        je.accountChild = AccountChild.objects.get(name='Merchandise Inventory')
        je.amount = purchase.amountDue
        je.accountChild.amount += je.amount
        je.accountChild.save()
        je.balance = je.accountChild.amount
        je.save()
        request.user.branch.journal.add(je)

        je = JournalEntries()

        if purchase.paymentPeriod == 'Full Payment':
            if purchase.paymentMethod == 'Cash on Hand':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journal.add(je)
            elif purchase.paymentMethod == 'Cash in Bank':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journal.add(je)
        elif purchase.paymentPeriod == 'Partial Payment':
            if purchase.paymentMethod == 'Cash on Hand':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journal.add(je)

                payables = JournalEntries()

                payables.journal = j
                payables.normally = "Credit"
                payables.accountChild = AccountChild.objects.get(name="Accounts Payables")
                payables.amount = purchase.amountDue - purchase.amountPaid
                payables.accountChild.amount += je.amount
                je.accountChild.save()
                payables.balance = je.accountChild.amount
                payables.save()
                request.user.branch.journal.add(payables)

            elif purchase.paymentMethod == 'Cash in Bank':
                je.journal = j
                je.normally = 'Credit'
                je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                je.amount = purchase.amountPaid
                je.accountChild.amount -= je.amount
                je.accountChild.save()
                je.balance = je.accountChild.amount
                je.save()
                request.user.branch.journal.add(je)

                payables = JournalEntries()

                payables.journal = j
                payables.normally = "Credit"
                payables.accountChild = AccountChild.objects.get(name="Accounts Payables")
                payables.amount = purchase.amountDue - purchase.amountPaid
                payables.accountChild.amount += je.amount
                je.accountChild.save()
                payables.balance = je.accountChild.amount
                payables.save()
                request.user.branch.journal.add(payables)
        

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
    


