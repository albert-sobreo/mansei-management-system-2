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

class PRVoid(APIView):
    def put(self, request, pk, format = None):
        pr = PurchaseRequest.objects.get(pk=pk)
        pr.voided = True
        pr.datetimeVoided = datetime.now()
        pr.voidedBy = request.user
        pr.save()

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

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        purchase.datetimeApproved = datetime.now()
        purchase.approved = True
        purchase.approvedBy = request.user

        purchase.save()
        
        if purchase.poitemsother.all():
            if purchase.needsRR == False:
                j = Journal()

                j.code = purchase.code
                j.datetimeCreated = purchase.datetimeApproved
                j.createdBy = purchase.createdBy
                j.journalDate = datetime.now()
                j.save()
                request.user.branch.journal.add(j)

                jeAPI(request, j, 'Credit', purchase.party.accountChild.get(name__regex=r"[Pp]ayable"), purchase.runningBalance)

                expenseType = {}
                for element in purchase.poitemsother.all():
                    if expenseType.get(element.type):
                        expenseType[element.type] += element.totalPrice
                    else:
                        expenseType[element.type] = element.totalPrice

                for key, val in expenseType.items():
                    jeAPI(request, j, "Debit", AccountChild.objects.get(name = key), (val/(1+(purchase.taxRate/100))))

                if purchase.taxPeso != 0:
                    jeAPI(request, j, "Debit", dChildAccount.inputVat, purchase.taxPeso)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class POVoid(APIView):
    def put(self, request, pk, format = None):
        purchase = PurchaseOrder.objects.get(pk=pk)
        purchase.voided = True
        purchase.voidedBy = request.user
        purchase.datetimeVoided = datetime.now()
        purchase.save()

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        if purchase.poitemsother.all():
            if purchase.needsRR == False:
                j = Journal()

                j.code = purchase.code
                j.datetimeCreated = purchase.datetimeVoided
                j.createdBy = purchase.voidedBy
                j.journalDate = datetime.now()
                j.save()
                request.user.branch.journal.add(j)

                jeAPI(request, j, 'Debit', purchase.party.accountChild.get(name__regex=r"[Pp]ayable"), purchase.runningBalance)

                expenseType = {}
                for element in purchase.poitemsother.all():
                    if expenseType.get(element.poitemsother.type):
                        expenseType[element.poitemsother.type] += element.poitemsother.totalPrice
                    else:
                        expenseType[element.poitemsother.type] = element.poitemsother.totalPrice

                for key, val in expenseType.items():
                    jeAPI(request, j, "Credit", AccountChild.objects.get(name = key), (val/(1+(purchase.taxRate/100))))

                if purchase.taxPeso != 0:
                    jeAPI(request, j, "Credit/", dChildAccount.inputVat, purchase.taxPeso)
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
        
        if receive.purchaseOrder.needsRR == True:
            fullyReceived = []
            merchAmountDue = Decimal(0)
            for element in receive.rritemsmerch.all():
                element.poitemsmerch.qtyReceived += element.qty
                if element.poitemsmerch.qtyReceived >= element.poitemsmerch.qty:
                    fullyReceived.append(1)
                else:
                    fullyReceived.append(0)
                if 0 not in fullyReceived:
                    element.poitemsmerch.purchaseOrder.fullyReceived = True
                    element.poitemsmerch.purchaseOrder.save()
                element.poitemsmerch.save()
                # element.merchInventory.qtyA += element.qty
                # element.merchInventory.qtyT = element.merchInventory.qtyA + element.merchInventory.qtyR
                wi = WarehouseItems.objects.get(merchInventory=element.merchInventory)
                wi.addQty(element.qty)
                element.merchInventory = MerchandiseInventory.objects.get(pk=element.merchInventory.pk)
                # print(element.merchInventory.qtyT, element.merchInventory.qtyA, element.merchInventory.pk)
                merchAmountDue += Decimal(element.totalPrice)
                element.merchInventory.totalCost += element.totalPrice                
                element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
                element.merchInventory.save()

            fullyReceived2 = []
            expenseAmountDue = {}
            for element in receive.rritemsother.all():
                element.poitemsother.qtyReceived += element.qty
                if element.poitemsother.qtyReceived >= element.poitemsother.qty:
                    fullyReceived2.append(1)

                else:
                    fullyReceived2.append(0)

                if 0 not in fullyReceived2:
                    element.poitemsother.purchaseOrder.fullyReceived = True
                    element.poitemsother.purchaseOrder.save()

                if expenseAmountDue.get(element.poitemsother.type):
                    expenseAmountDue[element.poitemsother.type] += element.poitemsother.totalPrice
                else:
                    expenseAmountDue[element.poitemsother.type] = element.poitemsother.totalPrice

                element.poitemsother.save()

                element.otherInventory.purchasingPrice = element.purchasingPrice
                element.otherInventory.qty += element.qty
                element.otherInventory.save()

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
                receive.first = True
                receive.save()
                if merchAmountDue:
                    jeAPI(request, j, 'Debit', dChildAccount.merchInventory, (merchAmountDue/(1+(receive.taxRate/100))))

                for key, val in expenseAmountDue.items():
                    if val:
                        jeAPI(request, j, 'Debit', AccountChild.objects.get(name=key), (val/(1+(receive.taxRate/100))))
            
                jeAPI(request, j, 'Debit', dChildAccount.inputVat, (receive.taxPeso))
    
                jeAPI(request, j, 'Credit', receive.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), receive.amountDue)

            else:
                if merchAmountDue:
                    jeAPI(request, j, 'Debit', dChildAccount.merchInventory, (merchAmountDue/(1+(receive.taxRate/100))))

                for key, val in expenseAmountDue.items():
                    if val:
                        jeAPI(request, j, 'Debit', AccountChild.objects.get(name=key), (val/(1+(receive.taxRate/100))))

                jeAPI(request, j, 'Credit', dChildAccount.prepaidExpense, (receive.amountDue - receive.taxPeso))

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class RRVoid(APIView):
    def put(self, request, pk, format = None):

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        rr = ReceivingReport.objects.get(pk=pk)
        rr.voided = True
        rr.datetimeVoided = datetime.now()
        rr.voidedBy = request.user

        merchAmountDue = Decimal(0)
        for element in rr.rritemsmerch.all():
            element.poitemsmerch.qtyReceived -= element.qty
            element.poitemsmerch.purchaseOrder.fullyReceived = False
            element.poitemsmerch.purchaseOrder.save()
            element.poitemsmerch.save()
            wi = WarehouseItems.objects.get(merchInventory=element.merchInventory)
            wi.addQty(-element.qty)
            element.merchInventory = MerchandiseInventory.objects.get(pk=element.merchInventory.pk)

            merchAmountDue += Decimal(element.totalPrice)
            element.merchInventory.totalCost += element.totalPrice                
            element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
            element.merchInventory.save()

        expenseAmountDue = {}
        for element in rr.rritemsother.all():
            element.poitemsother.qtyReceived -= element.qty
            element.poitemsother.purchaseOrder.fullyReceived = False
            element.poitemsother.purchaseOrder.save()

            if expenseAmountDue.get(element.poitemsother.type):
                expenseAmountDue[element.poitemsother.type] += element.poitemsother.totalPrice
            else:
                expenseAmountDue[element.poitemsother.type] = element.poitemsother.totalPrice

            element.poitemsother.save()

            element.otherInventory.qty -= element.qty
            element.otherInventory.save()
        rr.save()

        j = Journal()

        j.code = rr.code
        j.datetimeCreated = rr.datetimeVoided
        j.createdBy = rr.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        je = JournalEntries()

        if rr.first == True:
            if merchAmountDue:
                jeAPI(request, j, 'Credit', dChildAccount.merchInventory, (merchAmountDue/(1+(rr.taxRate/100))))
            
            for key, val in expenseAmountDue.items():
                if val:
                    jeAPI(request, j, 'Credit', AccountChild.objects.get(name=key), (val/(1+(rr.taxRate/100))))
        
            jeAPI(request, j, 'Credit', dChildAccount.inputVat, (rr.taxPeso))
 
            jeAPI(request, j, 'Debit', rr.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), rr.amountDue)

        else:
            if merchAmountDue:
                jeAPI(request, j, 'Credit', dChildAccount.merchInventory, (merchAmountDue/(1+(rr.taxRate/100))))
            
            for key, val in expenseAmountDue.items():
                if val:
                    jeAPI(request, j, 'Credit', AccountChild.objects.get(name=key), (val/(1+(rr.taxRate/100))))

            jeAPI(request, j, 'Debit', dChildAccount.prepaidExpense, (rr.amountDue - rr.taxPeso))

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

                wi = WarehouseItems.objects.get(merchInventory=merch)
                wi.addQty(element.qty)

                merch = MerchandiseInventory.objects.get(code=element.code)
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
                newMerch.inventoryDate = datetime.now()
                newMerch.save()
                wi = WarehouseItems()
                wi.merchInventory = newMerch
                wi.warehouse = Warehouse.objects.get(name='SBMA')
                wi.initQty(newMerch.qtyT, newMerch.qtyR, newMerch.qtyA)
                wi.save()
                request.user.branch.warehouseItems.add(wi)
                request.user.branch.merchInventory.add(newMerch)
        ii.save()       

        j = Journal()

        j.code = ii.code
        j.datetimeCreated = ii.datetimeApproved
        j.createdBy = ii.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        jeAPI(request, j, 'Debit', dChildAccount.merchInventory, (ii.amountTotal))

        jeAPI(request, j, 'Credit', ii.party.accountChild.get(name__regex=r"[Pp]ayable"), ii.amountTotal)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class IIVoid(APIView):
    def put(self, request, pk, format = None):
        ii = InwardInventory.objects.get(pk=pk)
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        ii.voided = True
        ii.datetimeVoided = datetime.now()
        ii.voidedBy = request.user
        
        for element in ii.iiadjusteditems.all():
            merch = MerchandiseInventory.objects.get(code = element.code)
            wi = WarehouseItems.objects.get(merchInventory = merch)
            wi.addQty(-element.qty)

            merch = MerchandiseInventory.objects.get(code=element.code)
            merch.totalCost -= element.totalCost
            merch.purchasingPrice = (Decimal(merch.totalCost / merch.qtyT))
            merch.save()
        ii.save()

        j = Journal()

        j.code = ii.code
        j.datetimeCreated = ii.datetimeApproved
        j.createdBy = ii.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        jeAPI(request, j, 'Credit', dChildAccount.merchInventory, (ii.amountTotal))

        jeAPI(request, j, 'Debit', ii.party.accountChild.get(name__regex=r"[Pp]ayable"), ii.amountTotal)

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

        if voucher.paymentMethod == "Cheque":
            voucher.cheque.approved = True
            voucher.cheque.datetimeApproved = datetime.now()
            voucher.cheque.approvedBy = request.user
            voucher.cheque.save()

        

        ################# EXPENSE PAYMENT #################
        if voucher.purchaseOrder.poitemsother.all():
            j = Journal()
            j.code = voucher.code
            j.datetimeCreated = voucher.datetimeApproved
            j.createdBy = voucher.createdBy
            j.journalDate = datetime.now()
            j.save()
            request.user.branch.journal.add(j)

            if voucher.purchaseOrder.needsRR == False:
                # ################# DEBIT SIDE #################
                # jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.amountPaid)

                
                if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                    jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)
                    jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.amountPaid)
                elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                    jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                    jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.amountPaid)
                elif voucher.paymentMethod == "Cheque":
                    jeAPI(request, j, 'Credit', voucher.cheque.accountChild, voucher.amountPaid)
                    jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.amountPaid)
                elif voucher.paymentMethod == "Memorandum":
                    voucher.transaction
                    if voucher.purchaseOrder.runningBalance <= voucher.transaction.runningBalance:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.purchaseOrder.runningBalance)
                        jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.purchaseOrder.runningBalance)
                    else:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.transaction.runningBalance)
                        jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.transaction.runningBalance)

            else:
                ################# DEBIT SIDE #################
                ################# IF FIRST PAYMENT #################
                if voucher.purchaseOrder.runningBalance == voucher.purchaseOrder.amountTotal:
                    voucher.first = True
                    voucher.save()
                    ################# IF RR WAS DONE BEFORE PV #################
                    if voucher.purchaseOrder.receivingreport.first():
                        ################# IF RR IS APPROVED #################
                        if voucher.purchaseOrder.receivingreport.first().approved == True:

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                        ################# IF RR IS NOT APPROVED UPON PV #################
                        else:
                            jeAPI(request, j, 'Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                            jeAPI(request, j, 'Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))

                    ################# IF PV IS DONE BEFORE RR #################
                    else:
                        jeAPI(request, j, 'Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                        jeAPI(request, j, 'Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))

                ################# IF NOT FIRST PAYMENT #################
                else:
                    jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                ################# CREDIT SIDE #################
                if voucher.wep != Decimal(0.0):
                    jeAPI(request, j, 'Credit', dChildAccount.ewp, voucher.wep)

                if voucher.paymentPeriod == 'Full Payment':
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)

                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Credit', voucher.cheque.accountChild, voucher.amountPaid)
                    
                elif voucher.paymentPeriod == 'Partial Payment':
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Credit', voucher.cheque.accountChild, voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                if voucher.paymentMethod == "Memorandum":
                    if voucher.purchaseOrder.runningBalance <= voucher.amountPaid:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.purchaseOrder.runningBalance)
                    else:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.amountPaid)
                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
        
        else:
        ################# MERCHANDISE PAYMENT #################
            ################# INWARD INVENTORY JOURNAL #################
            if voucher.purchaseOrder == None:
                j = Journal()
                j.code = voucher.code
                j.datetimeCreated = voucher.datetimeApproved
                j.createdBy = voucher.createdBy
                j.journalDate = datetime.now()
                j.save()
                request.user.branch.journal.add(j)

                jeAPI(request, j, 'Debit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.inwardInventory.runningBalance)

                if voucher.paymentPeriod == 'Full Payment':
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)

                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Credit', voucher.cheque.accountChild, voucher.amountPaid)

                elif voucher.paymentPeriod == 'Partial Payment':
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance - voucher.amountPaid))

                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance - voucher.amountPaid))
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance - voucher.amountPaid))
                    
                if voucher.paymentMethod == "Memorandum":
                    if voucher.inwardInventory.runningBalance <= voucher.transaction.runningBalance:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.inwardInventory.runningBalance)
                    else:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.amountPaid)
                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance - voucher.amountPaid))

                if voucher.inwardinventory.runningBalance == voucher.inwardinventory.amountTotal:
                    voucher.inwardinventory.first = True


            ################# PURCHASE ORDER JOURNAL #################
            else:
                j = Journal()
                j.code = voucher.code
                j.datetimeCreated = voucher.datetimeApproved
                j.createdBy = voucher.createdBy
                j.journalDate = datetime.now()
                j.save()
                request.user.branch.journal.add(j)

                ################# DEBIT SIDE #################
                ################# IF FIRST PAYMENT #################
                if voucher.purchaseOrder.runningBalance == voucher.purchaseOrder.amountTotal:
                    voucher.first = True
                    voucher.save()
                    ################# IF RR WAS DONE BEFORE PV #################
                    if voucher.purchaseOrder.receivingreport.first():
                        ################# IF RR IS APPROVED #################
                        if voucher.purchaseOrder.receivingreport.first().approved == True:

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                        ################# IF RR IS NOT APPROVED UPON PV #################
                        else:
                            jeAPI(request, j, 'Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                            jeAPI(request, j, 'Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))

                    ################# IF PV IS DONE BEFORE RR #################
                    else:
                        jeAPI(request, j, 'Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                        jeAPI(request, j, 'Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))

                ################# IF NOT FIRST PAYMENT #################
                else:
                    jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                voucher.purchaseOrder.wep += voucher.wep
                voucher.purchaseOrder.save()

                ################# CREDIT SIDE #################
                jeAPI(request, j, 'Credit', dChildAccount.ewp, voucher.wep)

                if voucher.paymentPeriod == 'Full Payment':
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)

                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Credit', voucher.cheque.accountChild, voucher.amountPaid)
                        
                elif voucher.paymentPeriod == 'Partial Payment':
                    print('b0ss plis')
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Credit', dChildAccount.cashOnHand, voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Credit', voucher.cheque.accountChild, voucher.amountPaid)

                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                if voucher.paymentMethod == "Memorandum":
                    if voucher.purchaseOrder.runningBalance <= voucher.amountPaid:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.purchaseOrder.runningBalance)
                    else:
                        jeAPI(request, j, 'Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.amountPaid)
                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

        if voucher.paymentMethod == "Memorandum":
            if voucher.purchaseOrder.runningBalance <= voucher.transaction.runningBalance:
                voucher.transaction.runningBalance -= voucher.purchaseOrder.runningBalance
                voucher.purchaseOrder.runningBalance = Decimal(0.0)
                voucher.purchaseOrder.fullyPaid == True
            else:
                voucher.purchaseOrder.runningBalance -= voucher.transaction.runningBalance
                voucher.transaction.runningBalance = Decimal(0.0)
                voucher.transaction.fullyPaid == True
            voucher.transaction.save()
        else:
            voucher.purchaseOrder.runningBalance -= voucher.amountPaid
            if voucher.purchaseOrder.runningBalance == 0:
                voucher.purchaseOrder.fullyPaid == True
        voucher.purchaseOrder.save()
        



        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class PVVoid(APIView):
    def put(self, request, pk, format = None):
        voucher = PaymentVoucher.objects.get(pk=pk)
        voucher.voided = True
        voucher.datetimeVoided = datetime.now()
        voucher.voidedBy = request.user
        
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        if voucher.paymentMethod == "Cheque":
            voucher.cheque.paymentVoucher = None
            voucher.cheque.paymentVoucher.save()


        ################# EXPENSE PAYMENT #################
        if voucher.purchaseOrder.poitemsother.all():
            if voucher.purchaseOrder.paymentvoucher.all().latest('pk') == voucher:
                j = Journal()
                j.code = voucher.code
                j.datetimeCreated = voucher.datetimeApproved
                j.createdBy = voucher.createdBy
                j.journalDate = datetime.now()
                j.save()
                request.user.branch.journal.add(j)

                if voucher.purchaseOrder.needsRR == False:
                    ################# CREDIT SIDE #################
                    jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.amountPaid)

                    ################# DEBIT SIDE #################
                    if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                        jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)
                    elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                        jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                    elif voucher.paymentMethod == "Cheque":
                        jeAPI(request, j, 'Debit', voucher.cheque.accountChild, voucher.amountPaid)
                else:
                    ################# CREDIT SIDE #################
                    if voucher.first == True:
                        ################# IF RR WAS DONE BEFORE PV ################
                        if voucher.purchaseOrder.receivingreport.first():
                            jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance + voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                        ################# IF PV IS DONE BEFORE RR ################
                        else:
                            jeAPI(request, j, 'Credit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                            jeAPI(request, j, 'Credit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))
                    ################# IF NOT FIRST PAYMENT #################
                    else:
                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance + voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                    voucher.purchaseOrder.wep -= voucher.wep
                    voucher.purchaseOrder.save()

                    ################# DEBIT SIDE #################
                    if voucher.wep != Decimal(0.0):
                        jeAPI(request, j, 'Debit', dChildAccount.ewp, voucher.wep)

                    if voucher.paymentPeriod == 'Full Payment':
                        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)

                        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                        elif voucher.paymentMethod == "Cheque":
                            jeAPI(request, j, 'Debit', voucher.cheque.accountChild, voucher.amountPaid)

                    elif voucher.paymentPeriod == 'Partial Payment':
                        print('b0ss plis')
                        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                        elif voucher.paymentMethod == "Cheque":
                            jeAPI(request, j, 'Debit', voucher.cheque.accountChild, voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                voucher.purchaseOrder.runningBalance += voucher.amountPaid
                voucher.purchaseOrder.fullyPaid == False
                voucher.purchaseOrder.save()
                voucher.purchaseOrder = None
                voucher.save()
                sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
                return JsonResponse(0, safe=False)
            else:
                sweetify.sweetalert(request, icon='warning', title='Error!', text = 'Not Latest Payment Voucher', persistent='Dismiss')
                return JsonResponse(0, safe=False)


        ################# MERCHANDISE PAYMENT #################
        else:
            ################# INWARD INVENTORY JOURNAL #################
            if voucher.purchaseOrder == None:
                if voucher.inwardInventory.paymentvoucher.all().latest('pk') == voucher:
                    j = Journal()
                    j.code = voucher.code
                    j.datetimeCreated = voucher.datetimeApproved
                    j.createdBy = voucher.createdBy
                    j.journalDate = datetime.now()
                    j.save()
                    request.user.branch.journal.add(j)

                    jeAPI(request, j, 'Credit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), voucher.inwardInventory.runningBalance + voucher.amountPaid)

                    if voucher.paymentPeriod == 'Full Payment':
                        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)

                        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                        elif voucher.paymentMethod == "Cheque":
                            jeAPI(request, j, 'Debit', voucher.cheque.accountChild, voucher.amountPaid)

                    elif voucher.paymentPeriod == 'Partial Payment':
                        # print('b0ss plis')
                        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance))

                        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance))
                        elif voucher.paymentMethod == "Cheque":
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.inwardInventory.party.accountChild.get(name__regex=r"[Pp]ayable"), (voucher.inwardInventory.runningBalance))

                    voucher.inwardInventory.runningBalance += voucher.amountPaid
                    voucher.inwardInventory.fullyPaid == False
                    voucher.inwardInventory.save()
                    voucher.inwardInventory = None
                    voucher.save()

                    sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
                    return JsonResponse(0, safe=False)
                else:
                    sweetify.sweetalert(request, icon='warning', title='Error!', text = 'Not Latest Payment Voucher', persistent='Dismiss')
                    return JsonResponse(0, safe=False)

            ################# PURCHASE ORDER JOURNAL #################
            else:
                if voucher.purchaseOrder.paymentvoucher.all().latest('pk') == voucher:
                    j = Journal()
                    j.code = voucher.code
                    j.datetimeCreated = voucher.datetimeApproved
                    j.createdBy = voucher.createdBy
                    j.journalDate = datetime.now()
                    j.save()
                    request.user.branch.journal.add(j)

                    ################# CREDIT SIDE #################wwwww
                    if voucher.first == True:
                        ################# IF RR WAS DONE BEFORE PV ################
                        if voucher.purchaseOrder.receivingreport.first():
                            jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance + voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                        ################# IF PV IS DONE BEFORE RR ################
                        else:
                            jeAPI(request, j, 'Credit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                            jeAPI(request, j, 'Credit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))
                    ################# IF NOT FIRST PAYMENT #################
                    else:
                        jeAPI(request, j, 'Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance + voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                    voucher.purchaseOrder.wep -= voucher.wep
                    voucher.purchaseOrder.save()

                    ################# DEBIT SIDE #################
                    jeAPI(request, j, 'Debit', dChildAccount.ewp, voucher.wep)

                    if voucher.paymentPeriod == 'Full Payment':
                        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)

                        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
                        elif voucher.paymentMethod == "Cheque":
                            jeAPI(request, j, 'Debit', voucher.cheque.accountChild, voucher.amountPaid)

                    elif voucher.paymentPeriod == 'Partial Payment':
                        print('b0ss plis')
                        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
                            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
                            jeAPI(request, j, 'Debit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
                        elif voucher.paymentMethod == "Cheque":
                            jeAPI(request, j, 'Debit', voucher.cheque.accountChild, voucher.amountPaid)

                            jeAPI(request, j, 'Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

                    voucher.purchaseOrder.runningBalance += voucher.amountPaid

                    voucher.purchaseOrder.fullyPaid == False
                    voucher.purchaseOrder.save()
                    voucher.purchaseOrder = None
                    voucher.save()
                    sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
                    return JsonResponse(0, safe=False)
                else:
                    sweetify.sweetalert(request, icon='warning', title='Error!', text = 'Not Latest Payment Voucher', persistent='Dismiss')
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
            wi = WarehouseItems.objects.filter(merchInventory=element.merchInventory)[0]
            wi.resQty(element.qty)
            # element.merchInventory.qtyT -= element.qty
            # element.merchInventory.qtyR += element.qty
            # element.merchInventory.qtyA = element.merchInventory.qtyT - element.merchInventory.qtyR
            # element.merchInventory.save()

        salesOrder.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SOVoid(APIView):
    def put(self, request, pk, format = None):
        salesOrder = SalesOrder.objects.get(pk=pk)
        salesOrder.voided = True
        salesOrder.datetimeVoided = datetime.now()
        salesOrder.voidedBy = request.user

        for element in salesOrder.soitemsmerch.all():
            wi = WarehouseItems.objects.get(merchInventory = element.merchInventory)
            wi.resQty(-element.qty)
            # element.merchInventory = MerchandiseInventory.objects.get(pk=element.merchInventory.pk)

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

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        
        if not sale.salesOrder:
            for element in sale.scitemsmerch.all():
                if element.merchInventory.qtyA <= element.qty:
                    sweetify.sweetalert(request, icon='error', title='Error', text="{} has {} items. You are selling {} items.".format((element.merchInventory.name + ' ' + element.merchInventory.classification + ' ' + element.merchInventory.type), element.merchInventory.qtyA, element.qty), persistent='Dismiss')
                    return JsonResponse(0, safe=False)
                else:
                    wi = WarehouseItems.objects.filter(merchInventory = element.merchInventory)[0]
                    wi.resQty(-element.qty)

        sale.datetimeApproved = datetime.now()
        sale.approved = True
        sale.approvedBy = request.user

        sale.save()

        j = Journal()

        j.code = sale.code
        j.datetimeCreated = sale.datetimeApproved
        j.createdBy = sale.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        
        totalFees = Decimal(0.0)

        for fees in sale.scotherfees.all():
            totalFees += fees.fee
        
        if totalFees != 0.0:
            jeAPI(request, j, 'Credit', dChildAccount.otherIncome, totalFees)

        if sale.taxPeso != 0.0:
            jeAPI(request, j, 'Credit', dChildAccount.outputVat, sale.taxPeso)

        jeAPI(request, j, 'Credit', dChildAccount.sales, sale.amountTotal - sale.taxPeso - totalFees)

        jeAPI(request, j, 'Debit', sale.party.accountChild.get(name__regex=r"[Rr]eceivable"), sale.amountTotal)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SCVoid(APIView):
    def put(self, request, pk, format = None):
        sale = SalesContract.objects.get(pk=pk)

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        sale.datetimeVoided = datetime.now()
        sale.voided = True
        sale.voidedBy = request.user
        
        if sale.receivepayment:
            for item in sale.receivepayment.all():
                item.voided = True
                item.save()

        sale.save()

        j = Journal()

        j.code = sale.code
        j.datetimeCreated = sale.datetimeApproved
        j.createdBy = sale.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        totalFees = Decimal(0.0)

        for fees in sale.scotherfees.all():
            totalFees += fees.fee

        if totalFees != 0.0:
            jeAPI(request, j, 'Debit', dChildAccount.otherIncome, totalFees)

        if sale.taxPeso != 0.0:
            jeAPI(request, j, 'Debit', dChildAccount.outputVat, sale.taxPeso)



        if sale.receivepayment.all():
            
            j2 = Journal()

            j2.code = sale.code
            j2.datetimeCreated = sale.datetimeApproved
            j2.createdBy = sale.createdBy
            j2.journalDate = datetime.now()
            j2.save()
            request.user.branch.journal.add(j2)

            toJournal = [{}]
            accountReceivable = Decimal(0.0)
            wep = Decimal(0.0)
            cashOnHand = Decimal(0.0)
            bankAccount = {}
            for rp in sale.receivepayment.all():
                
                accountReceivable += (rp.amountPaid + rp.wep)
                
                if rp.wep!= 0.0:
                    wep += rp.wep

                if rp.paymentMethod == dChildAccount.cashOnHand.name:
                    cashOnHand += rp.amountPaid
                elif re.search('[Cc]ash [Ii]n [Bb]ank', rp.paymentMethod):
                    if rp.paymentMethod in bankAccount:
                        bankAccount[rp.paymentMethod] += rp.amountPaid
                    else:
                        bankAccount[rp.paymentMethod] = rp.amountPaid
                rp.salesContract.runningBalance += (rp.amountPaid + rp.wep)
                rp.salesContract.fullyPaid = False
                rp.salesContract.save()

            ################# DEBIT SIDE #################
            jeAPI(request, j2, 'Debit', sale.party.accountChild.get(name__regex=r"[Rr]eceivable"), Decimal(accountReceivable))

            ################# CREDIT SIDE #################
            if wep != 0.0:
                jeAPI(request, j2, 'Credit', dChildAccount.cwit, Decimal(wep))
            if cashOnHand != 0.0:
                jeAPI(request, j2, 'Credit', dChildAccount.cashOnHand, Decimal(cashOnHand))
            for key, val in bankAccount.items():
                jeAPI(request, j2, 'Credit', dChildAccount.cashInBank.get(name=key), Decimal(val))
            # if cashInBank != 0.0:
                # jeAPI(request, j, 'Credit', dChildAccount.cashInBank.get(name=rp.paymentMethod), cashInBank)

        jeAPI(request, j, 'Debit', dChildAccount.sales, sale.amountTotal - sale.taxPeso - totalFees)

        jeAPI(request, j, 'Credit', sale.party.accountChild.get(name__regex=r"[Rr]eceivable"), sale.amountTotal)

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
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        deliveries = request.data
        d = Deliveries.objects.get(pk=pk)


        d.datetimeApproved = datetime.now()

        d.approvedBy = request.user
        d.approved = True
        d.truck.status = 'In-transit'
        d.truck.driver = d.driver
        d.driver.status = 'In-transit'
        d.truck.currentDelivery = d.pk
        d.truck.save()
        d.driver.save()
        d.save()

        
        for item in d.deliveryitemsgroup.all():
            if item.deliveryType == 'Sales Contract':
                sc = SalesContract.objects.get(pk=item.referenceNo)
                for element in sc.scitemsmerch.all():
                    # element.merchInventory.qtyA -= element.qty
                    # element.merchInventory.qtyT = element.merchInventory.qtyA - element.merchInventory.qtyR

                    wi = WarehouseItems.objects.get(merchInventory=element.merchInventory)
                    if sc.salesOrder:
                        wi.salesWSO(element.qty)
                    else:
                        wi.salesWOSO(element.qty)
                    element.merchInventory = MerchandiseInventory.objects.get(pk=element.merchInventory.pk)
                    element.merchInventory.totalCost -= element.totalCost                
                    # element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
                    element.merchInventory.save()

        j = Journal()

        j.code = d.code
        j.datetimeCreated = d.datetimeApproved
        j.createdBy = d.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        jeAPI(request, j, 'Credit', dChildAccount.merchInventory, d.amountTotal)

        jeAPI(request, j, 'Debit', dChildAccount.costOfSales, d.amountTotal)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class DeliveriesVoid(APIView):
    def put(self, request, pk, format = None):
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        d = Deliveries.objects.get(pk=pk)

        d.voided = True
        d.voidedBy = request.user
        d.datetimeVoided = datetime.now()

        d.truck.status = "Available"
        # print(d.truck.driver)
        d.truck.driver.status = "Available"
        d.truck.driver.save()
        d.truck.driver = None
        d.truck.currentDelivery = None
        d.truck.save()
        d.save()

        for item in d.deliveryitemsgroup.all():
            if item.deliveryType == 'Sales Contract':
                sc = SalesContract.objects.get(pk=item.referenceNo)
                for element in sc.scitemsmerch.all():
                    # element.merchInventory.qtyA -= element.qty
                    # element.merchInventory.qtyT = element.merchInventory.qtyA - element.merchInventory.qtyR

                    wi = WarehouseItems.objects.get(merchInventory=element.merchInventory)
                    if sc.salesOrder:
                        wi.salesWSO(-element.qty)
                    else:
                        wi.addQty(element.qty)
                    element.merchInventory = MerchandiseInventory.objects.get(pk=element.merchInventory.pk)
                    element.merchInventory.totalCost += element.totalCost                
                    # element.merchInventory.purchasingPrice = (Decimal(element.merchInventory.totalCost / element.merchInventory.qtyT))
                    element.merchInventory.save()

        j = Journal()

        j.code = d.code
        j.datetimeCreated = d.datetimeApproved
        j.createdBy = d.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        jeAPI(request, j, 'Debit', dChildAccount.merchInventory, d.amountTotal)

        jeAPI(request, j, 'Credit', dChildAccount.costOfSales, d.amountTotal)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)



################# TRANSFER AND ADJUSTMENT #################
class TransferNonApproved(View):
    def get(self, request, format=None):
        context = {
            'transfers': request.user.branch.transfer.filter(approved=False)
        }
        return render(request, 'tr-nonapproved.html', context)

class TransferApproved(View):
    def get(self, request, format=None):
        context = {
            'transfer': request.user.branch.transfer.filter(approved=True)
        }
        return render(request, 'tr-approved.html', context)

class TransferApproval(APIView):
    def put(self, request, pk, format = None):

        tr = Transfer.objects.get(pk=pk)

        tr.datetimeApproved = datetime.now()
        tr.approvedBy = request.user
        tr.approved = True

        for element in tr.tritems.all():
            ow = WarehouseItems.objects.get(merchInventory=element.merchInventory, warehouse=element.oldWarehouse)
            ow.addQty(-element.qtyTransfered)
            try:
                nw = WarehouseItems.objects.get(merchInventory=element.merchInventory, warehouse=tr.newWarehouse)
                nw.addQty(element.qtyTransfered)
            except:
                nw = WarehouseItems()
                nw.merchInventory = element.merchInventory
                nw.warehouse = tr.newWarehouse
                nw.initQty(nw.merchInventory.qtyT, nw.merchInventory.qtyR, nw.merchInventory.qtyA)
                nw.save()
                nw.addQty(element.qtyTransfered)
            # element.merchInventory.warehouse = tr.newWarehouse
            # element.merchInventory.save()

        tr.save()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class AdjustmentsNonApproved(View):
    def get(self, request, format=None):
        context = {
            'adjusts': request.user.branch.adjustments.filter(approved=False)
        }
        return render(request, 'ad-nonapproved.html', context)

class AdjustmentsApproved(View):
    def get(self, request, format=None):
        context = {
            'adjusts': request.user.branch.adjustments.filter(approved=True)
        }
        return render(request, 'ad-approved.html', context)

class AdjustmentApproval(APIView):
    def put(self, request, pk, format = None):

        ad = Adjustments.objects.get(pk=pk)

        ad.datetimeApproved = datetime.now()
        ad.approvedBy = request.user
        ad.approved = True

        for element in ad.aditems.all():
            # element.merchInventory.qtyA -= element.qtyAdjusted                                       
            # element.merchInventory.qtyT -= element.qtyAdjusted
            wi = WarehouseItems.objects.get(merchInventory = element.merchInventory, warehouse=element.oldWarehouse)
            wi.addQty(-element.qtyAdjusted)
            element.merchInventory = MerchandiseInventory.objects.get(pk=element.merchInventory.pk)
            element.merchInventory.totalCost -= element.totalCost
            element.merchInventory.save()

        ad.save()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)





########## BANK RECONCILIATION ##########
class BankReconNonApproved(View):
    def get(self, request, format=None):
        context = {
            'cheques': request.user.branch.cheque.filter(approved = False)
        }

        return render(request, 'bank-recon-non-approved.html', context)

class BankReconApproved(View):
    def get(self, request, format=None):
        context = {
            'cheques': request.user.branch.cheque.filter(approved = True)
        }

        return render(request, 'bank-recon-approved.html', context)
class BankReconApprovalAPI(APIView):
    def put(self, request, pk, format=None):
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        cheque = Cheques.objects.get(pk=pk)
        
        cheque.approved = True
        cheque.datetimeApproved = datetime.now()
        cheque.approvedBy = request.user
        cheque.save()

        j = Journal()
        j.datetimeCreated = cheque.datetimeApproved
        j.createdBy = cheque.approvedBy
        j.journalDate = datetime.now()
        j.save()

        cheque.receivePayment.journal = j
        cheque.receivePayment.save()
        request.user.branch.journal.add(j)

        ################# CREDIT SIDE #################
        jeAPI(request, j, 'Credit', cheque.receivePayment.salesContract.party.accountChild.get(name__regex=r"[Rr]eceivable"), (cheque.receivePayment.amountPaid + cheque.receivePayment.wep))

        ################# DEBIT SIDE #################
        if cheque.receivePayment.wep != 0.0:
            jeAPI(request, j, 'Debit', dChildAccount.cwit, cheque.receivePayment.wep)


        jeAPI(request, j, 'Debit', cheque.accountChild, cheque.receivePayment.amountPaid)

        cheque.receivePayment.salesContract.runningBalance -= (cheque.receivePayment.amountPaid + cheque.receivePayment.wep)
        if cheque.receivePayment.salesContract.runningBalance == 0:
            cheque.receivePayment.salesContract.fullyPaid = True
        cheque.receivePayment.salesContract.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)