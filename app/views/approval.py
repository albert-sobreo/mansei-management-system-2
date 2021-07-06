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
import re

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
        
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        receive = ReceivingReport.objects.get(pk=pk)

        receive.datetimeApproved = datetime.now()
        receive.approved = True
        receive.approvedBy = request.user
        
        fullyReceived = []
        for element in receive.rritemsmerch.all():
            element.poitemsmerch.qtyReceived += element.qty
            if element.poitemsmerch.qtyReceived == element.poitemsmerch.qty:
                fullyReceived.append(1)
            else:
                fullyReceived.append(0)
            if 0 not in fullyReceived:
                element.poitemsmerch.purchaseOrder.fullyReceived = True
                element.poitemsmerch.purchaseOrder.save()
            element.poitemsmerch.save()
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

        if receive.purchaseOrder.runningBalance == receive.purchaseOrder.amountTotal:
            je.journal = j
            je.normally = 'Debit'
            # je.accountChild = AccountChild.objects.get(name='Merchandise Inventory')
            je.accountChild = dChildAccount.merchInventory
            je.amount = receive.amountDue - receive.taxPeso
            je.accountChild.amount += je.amount
            je.accountChild.accountSubGroup.amount += je.amount
            je.accountChild.accountSubGroup.accountGroup.amount += je.amount
            je.accountChild.save()
            je.accountChild.accountSubGroup.save()
            je.accountChild.accountSubGroup.accountGroup.save()
            je.balance = je.accountChild.amount
            je.save()
            request.user.branch.journalEntries.add(je)

            vat = JournalEntries()
            vat.journal = j
            vat.normally = 'Debit'
            vat.accountChild = dChildAccount.inputVat
            vat.amount = receive.taxPeso
            vat.accountChild.amount += vat.amount
            vat.accountChild.accountSubGroup.amount += vat.amount
            vat.accountChild.accountSubGroup.accountGroup.amount += vat.amount
            vat.accountChild.save()
            vat.accountChild.accountSubGroup.save()
            vat.accountChild.accountSubGroup.accountGroup.save()
            vat.balance = vat.accountChild.amount
            vat.save()
            request.user.branch.journalEntries.add(vat)

            payables = JournalEntries()
            payables.journal = j
            payables.normally = 'Credit'
            payables.amount = receive.amountDue
            payables.accountChild = receive.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable")
            payables.accountChild.accountSubGroup.amount += payables.amount
            payables.accountChild.accountSubGroup.accountGroup.amount += payables.amount
            payables.accountChild.save()
            payables.accountChild.accountSubGroup.save()
            payables.accountChild.accountSubGroup.accountGroup.save()
            payables.balance = payables.accountChild.amount
            payables.save()
            request.user.branch.journalEntries.add(payables)



        else: 
            je.journal = j
            je.normally = 'Debit'
            # je.accountChild = AccountChild.objects.get(name='Merchandise Inventory')
            je.accountChild = dChildAccount.merchInventory
            je.amount = receive.amountDue - receive.taxPeso
            je.accountChild.amount += je.amount
            je.accountChild.accountSubGroup.amount += je.amount
            je.accountChild.accountSubGroup.accountGroup.amount += je.amount
            je.accountChild.save()
            je.accountChild.accountSubGroup.save()
            je.accountChild.accountSubGroup.accountGroup.save()
            je.balance = je.accountChild.amount
            je.save()
            request.user.branch.journalEntries.add(je)

            
            pe = JournalEntries()
            pe.journal = j
            pe.normally = 'Credit'
            pe.accountChild = dChildAccount.prepaidExpense
            pe.amount = receive.amountDue - receive.taxPeso
            pe.accountChild.amount -= pe.amount
            pe.accountChild.accountSubGroup.amount -= pe.amount
            pe.accountChild.accountSubGroup.accountGroup.amount -= pe.amount
            pe.accountChild.save()
            pe.accountChild.accountSubGroup.save()
            pe.accountChild.accountSubGroup.accountGroup.save()
            pe.balance = pe.accountChild.amount
            pe.save()
            request.user.branch.journalEntries.add(pe)


        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

################# INWARD INVENTORY #################
class IIapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'inward': user.branch.inwardInventory.filter(approved=True, adjusted=True),
        }
        return render(request, 'ii-approved.html', context)

class IInonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'inward': user.branch.inwardInventory.filter(approved=False, adjusted=True),
        }
        return render(request, 'ii-nonapproved.html', context)

class IIApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        ii = InwardInventory.objects.get(pk=pk)
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        ii.datetimeApproved = datetime.now()
        ii.approved = True
        ii.approvedBy = request.user

        for element in ii.iiadjusteditems.all():
            if MerchandiseInventory.objects.filter(code=element.code):
                merch = MerchandiseInventory.objects.get(code=element.code)
                merch.qtyA += element.qty
                merch.qtyT = merch.qtyA + merch.qtyR
                merch.totalCost += element.totalCost
                merch.purchasingPrice = (Decimal(merch.totalCost / merch.qtyT))
                merch.save()
            else:
                newMerch = MerchandiseInventory()
                newMerch.code = element.code
                newMerch.name = element.name
                newMerch.classification = element.classfication
                newMerch.type = element.type
                newMerch.length = element.length
                newMerch.width = element.width
                newMerch.thickness = element.thicc
                newMerch.vol = element.vol
                newMerch.qtyT = element.qty
                newMerch.qtyA = element.qty
                newMerch.qtyR = 0
                newMerch.totalCost = element.totalCost
                newMerch.purchasingPrice = (Decimal(element.totalCost / element.qty))
                newMerch.sellingPrice = 0.0
                newMerch.pricePerCubic = element.pricePerCubic
                newMerch.save()
                request.user.branch.merchInventory.add(newMerch)
        ii.save()       

        j = Journal()

        j.code = ii.code
        j.datetimeCreated = ii.datetimeApproved
        j.createdBy = ii.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        je = JournalEntries()
        je.journal = j
        je.normally = 'Debit'
        je.accountChild = dChildAccount.merchInventory
        je.amount = ii.amountTotal
        je.accountChild.amount += je.amount
        je.accountChild.accountSubGroup.amount += je.amount
        je.accountChild.accountSubGroup.accountGroup.amount += je.amount
        je.accountChild.save()
        je.accountChild.accountSubGroup.save()
        je.accountChild.accountSubGroup.accountGroup.save()
        je.balance = je.accountChild.amount
        je.save()
        request.user.branch.journalEntries.add(je)

        payables = JournalEntries()
        payables.journal = j
        payables.normally = 'Credit'
        payables.amount = ii.amountTotal
        payables.accountChild = ii.party.accountChild.get(name__regex=r"[Pp]ayable")
        payables.accountChild.accountSubGroup.amount += payables.amount
        payables.accountChild.accountSubGroup.accountGroup.amount += payables.amount
        payables.accountChild.save()
        payables.accountChild.accountSubGroup.save()
        payables.accountChild.accountSubGroup.accountGroup.save()
        payables.balance = payables.accountChild.amount
        payables.save()
        request.user.branch.journalEntries.add(payables)
        

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

################# PAYMENT VOUCHER #################
class PVapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'voucher': user.branch.paymentVoucher.filter(approved=True),
        }
        return render(request, 'pv-approved.html', context)

class PVnonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'voucher': user.branch.paymentVoucher.filter(approved=False),
        }
        return render(request, 'pv-nonapproved.html', context)

class PVApprovalAPI(APIView):
    def put(self, request, pk, format = None):
        voucher = PaymentVoucher.objects.get(pk=pk)

        voucher.datetimeApproved = datetime.now()
        voucher.approved = True
        voucher.approvedBy = request.user

        voucher.save()
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        if voucher.purchaseOrder == None:
            j = Journal()
            j.code = voucher.code
            j.datetimeCreated = voucher.datetimeApproved
            j.createdBy = voucher.createdBy
            j.journalDate = datetime.now()
            j.save()
            request.user.branch.journal.add(j)

            payables = JournalEntries()
            payables.journal = j
            payables.normally = 'Debit'
            payables.amount = voucher.inwardInventory.runningBalance
            payables.accountChild = voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable")
            payables.accountChild.accountSubGroup.amount += payables.amount
            payables.accountChild.accountSubGroup.accountGroup.amount += payables.amount
            payables.accountChild.save()
            payables.accountChild.accountSubGroup.save()
            payables.accountChild.accountSubGroup.accountGroup.save()
            payables.balance = payables.accountChild.amount
            payables.save()
            request.user.branch.journalEntries.add(payables)

            je = JournalEntries()

            if voucher.paymentPeriod == 'Full Payment':
                if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                    je.accountChild = dChildAccount.cashOnHand
                    je.amount = voucher.amountPaid
                    je.accountChild.amount -= je.amount
                    je.accountChild.accountSubGroup.amount -= je.amount
                    je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                    je.accountChild.save()
                    je.accountChild.accountSubGroup.save()
                    je.accountChild.accountSubGroup.accountGroup.save()
                    je.balance = je.accountChild.amount
                    je.save()
                    request.user.branch.journalEntries.add(je)
                elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                    je.accountChild = dChildAccount.cashInBank.get(name=voucher.paymentMethod)
                    je.amount = voucher.amountPaid
                    je.accountChild.amount -= je.amount
                    je.accountChild.accountSubGroup.amount -= je.amount
                    je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                    je.accountChild.save()
                    je.accountChild.accountSubGroup.save()
                    je.accountChild.accountSubGroup.accountGroup.save()
                    je.balance = je.accountChild.amount
                    je.save()
                    request.user.branch.journalEntries.add(je)
            elif voucher.paymentPeriod == 'Partial Payment':
                print('b0ss plis')
                if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                    je.accountChild = dChildAccount.cashOnHand
                    je.amount = voucher.amountPaid
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
                    payables.accountChild = voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable")
                    payables.amount = (voucher.inwardInventory.runningBalance - voucher.amountPaid)
                    payables.accountChild.amount += je.amount
                    payables.accountChild.accountSubGroup.amount += je.amount
                    payables.accountChild.accountSubGroup.accountGroup.amount += je.amount
                    payables.accountChild.save()
                    payables.accountChild.accountSubGroup.save()
                    payables.accountChild.accountSubGroup.accountGroup.save()
                    payables.balance = je.accountChild.amount
                    payables.save()
                    request.user.branch.journalEntries.add(payables)
                #elif purchase.paymentMethod == 'Cash in Bank':
                elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                    je.accountChild = dChildAccount.cashInBank.get(name=voucher.paymentMethod)
                    je.amount = voucher.amountPaid
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
                    ############
                    # payables.accountChild = purchase.party.accountChild.get(name__regex=r"[Pp]ayable")
                    # ########.accountChild = purchase.party.accountChild.get(name__regex=r"[Rr]eceivable")
                    ############
                    payables.accountChild = voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable")
                    payables.amount = (voucher.inwardInventory.runningBalance - voucher.amountPaid)
                    payables.accountChild.amount += je.amount
                    payables.accountChild.accountSubGroup.amount += je.amount
                    payables.accountChild.accountSubGroup.accountGroup.amount += je.amount
                    payables.accountChild.save()
                    payables.accountChild.accountSubGroup.save()
                    payables.accountChild.accountSubGroup.accountGroup.save()
                    payables.balance = je.accountChild.amount
                    payables.save()
                    request.user.branch.journalEntries.add(payables)            
            voucher.inwardInventory.runningBalance -= voucher.amountPaid
            voucher.inwardInventory.save()
            if voucher.inwardInventory.runningBalance == 0:
                voucher.inwardInventory.fullyPaid == True
        else:
            j = Journal()
            j.code = voucher.code
            j.datetimeCreated = voucher.datetimeApproved
            j.createdBy = voucher.createdBy
            j.journalDate = datetime.now()
            j.save()
            request.user.branch.journal.add(j)

            if voucher.purchaseOrder.runningBalance == voucher.purchaseOrder.amountTotal:
                if voucher.purchaseOrder.receivingreport.first() != None:
                    if voucher.purchaseOrder.receivingreport.first().approve == True:
                        payables = JournalEntries()
                        payables.journal = j
                        payables.normally = 'Debit'
                        payables.amount = (voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)
                        payables.accountChild = voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable")
                        payables.accountChild.accountSubGroup.amount += payables.amount
                        payables.accountChild.accountSubGroup.accountGroup.amount += payables.amount
                        payables.accountChild.save()
                        payables.accountChild.accountSubGroup.save()
                        payables.accountChild.accountSubGroup.accountGroup.save()
                        payables.balance = payables.accountChild.amount
                        payables.save()
                        request.user.branch.journalEntries.add(payables)
                    else:
                        vat = JournalEntries()
                        vat.journal = j
                        vat.normally = 'Debit'
                        # vat.accountChild = AccountChild.objects.get(name="VAT Amount")
                        vat.accountChild = dChildAccount.inputVat
                        vat.amount = voucher.purchaseOrder.taxPeso
                        vat.accountChild.accountSubGroup.amount += vat.amount
                        vat.accountChild.accountSubGroup.accountGroup.amount += vat.amount
                        vat.accountChild.save()
                        vat.accountChild.accountSubGroup.save()
                        vat.accountChild.accountSubGroup.accountGroup.save()
                        vat.balance = vat.accountChild.amount
                        vat.save()
                        request.user.branch.journalEntries.add(vat)

                        pe = JournalEntries()
                        pe.journal = j
                        pe.normally = 'Debit'
                        pe.accountChild = dChildAccount.prepaidExpense
                        pe.amount = voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso
                        pe.accountChild.amount += pe.amount
                        pe.accountChild.accountSubGroup.amount += pe.amount
                        pe.accountChild.accountSubGroup.accountGroup.amount += pe.amount
                        pe.accountChild.save()
                        pe.accountChild.accountSubGroup.save()
                        pe.accountChild.accountSubGroup.accountGroup.save()
                        pe.balance = pe.accountChild.amount
                        pe.save()
                        request.user.branch.journalEntries.add(pe)
                else:
                    vat = JournalEntries()
                    vat.journal = j
                    vat.normally = 'Debit'
                    # vat.accountChild = AccountChild.objects.get(name="VAT Amount")
                    vat.accountChild = dChildAccount.inputVat
                    vat.amount = voucher.purchaseOrder.taxPeso
                    vat.accountChild.accountSubGroup.amount += vat.amount
                    vat.accountChild.accountSubGroup.accountGroup.amount += vat.amount
                    vat.accountChild.save()
                    vat.accountChild.accountSubGroup.save()
                    vat.accountChild.accountSubGroup.accountGroup.save()
                    vat.balance = vat.accountChild.amount
                    vat.save()
                    request.user.branch.journalEntries.add(vat)

                    pe = JournalEntries()
                    pe.journal = j
                    pe.normally = 'Debit'
                    pe.accountChild = dChildAccount.prepaidExpense
                    pe.amount = voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso
                    pe.accountChild.amount += pe.amount
                    pe.accountChild.accountSubGroup.amount += pe.amount
                    pe.accountChild.accountSubGroup.accountGroup.amount += pe.amount
                    pe.accountChild.save()
                    pe.accountChild.accountSubGroup.save()
                    pe.accountChild.accountSubGroup.accountGroup.save()
                    pe.balance = pe.accountChild.amount
                    pe.save()
                    request.user.branch.journalEntries.add(pe)
            else:
                payables = JournalEntries()
                payables.journal = j
                payables.normally = 'Debit'
                payables.amount = (voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)
                payables.accountChild = voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable")
                payables.accountChild.accountSubGroup.amount += payables.amount
                payables.accountChild.accountSubGroup.accountGroup.amount += payables.amount
                payables.accountChild.save()
                payables.accountChild.accountSubGroup.save()
                payables.accountChild.accountSubGroup.accountGroup.save()
                payables.balance = payables.accountChild.amount
                payables.save()
                request.user.branch.journalEntries.add(payables)

            voucher.purchaseOrder.wep += voucher.wep
            voucher.purchaseOrder.save()
            wep = JournalEntries()
            wep.journal = j
            wep.normally = 'Credit'
            # wep.accountChild = AccountChild.objects.get(name="Withholding Expanded Payables")
            wep.accountChild = dChildAccount.ewp
            wep.amount = voucher.wep
            wep.accountChild.amount = wep.amount
            wep.accountChild.accountSubGroup.amount += wep.amount
            wep.accountChild.accountSubGroup.accountGroup.amount += wep.amount
            wep.accountChild.save()
            wep.accountChild.accountSubGroup.save()
            wep.accountChild.accountSubGroup.accountGroup.save()
            wep.balance = wep.accountChild.amount
            wep.save()
            request.user.branch.journalEntries.add(wep)
            
            je = JournalEntries()
            
            if voucher.paymentPeriod == 'Full Payment':
                if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                    je.accountChild = dChildAccount.cashOnHand
                    je.amount = voucher.amountPaid
                    je.accountChild.amount -= je.amount
                    je.accountChild.accountSubGroup.amount -= je.amount
                    je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                    je.accountChild.save()
                    je.accountChild.accountSubGroup.save()
                    je.accountChild.accountSubGroup.accountGroup.save()
                    je.balance = je.accountChild.amount
                    je.save()
                    request.user.branch.journalEntries.add(je)
                elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                    je.accountChild = dChildAccount.cashInBank.get(name=voucher.paymentMethod)
                    je.amount = voucher.amountPaid
                    je.accountChild.amount -= je.amount
                    je.accountChild.accountSubGroup.amount -= je.amount
                    je.accountChild.accountSubGroup.accountGroup.amount -= je.amount
                    je.accountChild.save()
                    je.accountChild.accountSubGroup.save()
                    je.accountChild.accountSubGroup.accountGroup.save()
                    je.balance = je.accountChild.amount
                    je.save()
                    request.user.branch.journalEntries.add(je)
            elif voucher.paymentPeriod == 'Partial Payment':
                print('b0ss plis')
                if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash on Hand")
                    je.accountChild = dChildAccount.cashOnHand
                    je.amount = voucher.amountPaid
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
                    payables.accountChild = voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable")
                    payables.amount = (voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)
                    payables.accountChild.amount += je.amount
                    payables.accountChild.accountSubGroup.amount += je.amount
                    payables.accountChild.accountSubGroup.accountGroup.amount += je.amount
                    payables.accountChild.save()
                    payables.accountChild.accountSubGroup.save()
                    payables.accountChild.accountSubGroup.accountGroup.save()
                    payables.balance = je.accountChild.amount
                    payables.save()
                    request.user.branch.journalEntries.add(payables)
                #elif purchase.paymentMethod == 'Cash in Bank':
                elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                    je.journal = j
                    je.normally = 'Credit'
                    # je.accountChild = AccountChild.objects.get(name="Cash in Bank")
                    je.accountChild = dChildAccount.cashInBank.get(name=voucher.paymentMethod)
                    je.amount = voucher.amountPaid
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
                    ############
                    # payables.accountChild = purchase.party.accountChild.get(name__regex=r"[Pp]ayable")
                    # ########.accountChild = purchase.party.accountChild.get(name__regex=r"[Rr]eceivable")
                    ############
                    payables.accountChild = voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable")
                    payables.amount = (voucher.purchaseOrder.runningBalance - voucher.amountPaid) - (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)
                    payables.accountChild.amount += je.amount
                    payables.accountChild.accountSubGroup.amount += je.amount
                    payables.accountChild.accountSubGroup.accountGroup.amount += je.amount
                    payables.accountChild.save()
                    payables.accountChild.accountSubGroup.save()
                    payables.accountChild.accountSubGroup.accountGroup.save()
                    payables.balance = je.accountChild.amount
                    payables.save()
                    request.user.branch.journalEntries.add(payables)            
            voucher.purchaseOrder.runningBalance -= voucher.amountPaid
            voucher.purchaseOrder.save()
            if voucher.purchaseOrder.runningBalance == 0:
                voucher.purchaseOrder.fullyPaid == True


        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)        

################# QUOTATIONS #################
class QQapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'quotes': user.branch.quotations.filter(approved=True),
        }
        return render(request, 'qq-approved.html', context)

class QQnonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'quotes': user.branch.quotations.filter(approved=False),
        }
        return render(request, 'qq-nonapproved.html', context)

class QQApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        quotes = Quotations.objects.get(pk=pk)

        quotes.datetimeApproved = datetime.now()
        quotes.approved = True
        quotes.approvedBy = request.user
        quotes.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

################# SALES ORDER #################
class SOapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'salesorder': user.branch.salesOrder.filter(approved=True),
        }
        return render(request, 'so-approved.html', context)

class SOnonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'salesorder': user.branch.salesOrder.filter(approved=False),
        }
        return render(request, 'so-nonapproved.html', context)

class SOApprovalAPI(APIView):
    def put(self, request, pk, format = None):

        salesOrder = SalesOrder.objects.get(pk=pk)

        salesOrder.datetimeApproved = datetime.now()
        salesOrder.approved = True
        salesOrder.approvedBy = request.user
        salesOrder.save()

        for element in salesOrder.soitemsmerch.all():
            element.merchInventory.qtyT -= element.qty
            element.merchInventory.qtyR += element.qty
            element.merchInventory.qtyA = element.merchInventory.qtyT - element.merchInventory.qtyR
            element.merchInventory.save()

        salesOrder.save()

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

        sale = SalesContract.objects.get(pk=pk)

        for element in sale.scitemsmerch.all():
            if element.merchInventory.qtyA == 0:
                print('b0ss')
                sweetify.sweetalert(request, icon='error', title='Error', text="{} has {} items. You are selling {} items.".format((element.merchInventory.name + ' ' + element.merchInventory.classification + ' ' + element.merchInventory.type), element.merchInventory.qtyA, element.qty), persistent='Dismiss')
                return JsonResponse(0, safe=False)

        sale.datetimeApproved = datetime.now()
        sale.approved = True
        sale.approvedBy = request.user


        for element in sale.scitemsmerch.all():
            element.merchInventory.qtyA -= element.qty
            element.merchInventory.qtyT = element.merchInventory.qtyA - element.merchInventory.qtyR
            element.merchInventory.totalCost += element.totalCost                
            # element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
            element.merchInventory.save()

        sale.save()

        # j = Journal()

        # j.code = sale.code
        # j.datetimeCreated = sale.datetimeApproved
        # j.createdBy = sale.createdBy
        # j.journalDate = datetime.now()
        # j.save()
        # request.user.branch.journal.add(j)

        # je = JournalEntries()

        # je.journal = j
        # je.normally = 'Credit'
        # je.accountChild = AccountChild.objects.get(name='Merchandise Inventory')
        # je.amount = sale.amountTotal
        # je.accountChild.amount -= je.amount
        # je.accountChild.save()
        # je.balance = je.accountChild.amount
        # je.save()
        # request.user.branch.journalEntries.add(je)

        # je = JournalEntries()

        # je.journal = j
        # je.normally = 'Debit'
        # je.accountChild = AccountChild.objects.get(name="Cash on Hand")
        # je.amount = sale.amountTotal
        # je.accountChild.amount += je.amount
        # je.accountChild.save()
        # je.balance = je.accountChild.amount
        # je.save()
        # request.user.branch.journalEntries.add(je)

        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

################# SALES INVOICE #################
class SIapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'invoice': user.branch.salesInvoice.filter(approved=True),
        }
        return render(request, 'si-approved.html', context)

class SInonapprovedView(View):
    def get(self, request, format=None):

        user = request.user
        context = {
            'invoice': user.branch.salesInvoice.filter(approved=False),
        }
        return render(request, 'si-nonapproved.html', context)

class SIApprovalAPI(APIView):
    def put(self, request, pk, format = None):
        invoice = SalesInvoice.objects.get(pk=pk)

        invoice.datetimeApproved = datetime.now()
        invoice.approved = True
        invoice.approvedBy = request.user

        invoice.save()
        


        

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