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
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class ADVapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        user = request.user
        context = {
            'advs': user.branch.advancementThruPettyCash.filter(approved = True),
        }
        return render(request, 'adv-approved.html', context)

class ADVnonapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        user = request.user
        context = {
            'advs': user.branch.advancementThruPettyCash.filter(approved = False),
        }
        return render(request, 'adv-nonapproved.html', context)

class ADVapprovalAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        adv = AdvancementThruPettyCash.objects.get(pk=request.data['id'])
        adv.approved = True
        adv.approvedBy = request.user
        adv.datetimeApproved = datetime.datetime.now()
        adv.save()

        j = Journal()

        j.code = adv.code
        j.datetimeCreated = adv.datetimeApproved
        j.createdBy = adv.issuer
        j.journalDate = datetime.date.today()
        j.save()

        request.user.branch.journal.add(j)

        jeAPI(request, j, 'Credit', dChildAccount.pettyCash, adv.amount)
        try:
            jeAPI(request, j, 'Debit', adv.requestor.employeeAccounts.get(name__regex=r"[Ad]dvance"), adv.amount)
        except:
            emploAcc = AccountChild()
            try:
                emploAcc.me = AccountChild.objects.get(name='Advances to Employee')
            except Exception as e:
                print(e)
                advToEm = AccountChild()
                advToEm.name = 'Advances to Employee'
                advToEm.accountSubGroup = request.user.branch.subGroup.get(name="Accounts Receivable")
                advToEm.amount = Decimal(0)
                advToEm.save()
                emploAcc.me = advToEm
            emploAcc.name = 'Advances to Employee - ' + adv.requestor.first_name + ' ' + adv.requestor.last_name
            emploAcc.accountSubGroup = request.user.branch.subGroup.get(name="Accounts Receivable")
            emploAcc.amount = Decimal(0)
            emploAcc.save()
            request.user.branch.accountChild.add(emploAcc)
            adv.requestor.employeeAccounts.add(emploAcc)
            jeAPI(request, j, 'Debit',emploAcc, adv.amount)

        notify(request, 'Advancement approved', adv.code, '/adv-approved/', 1)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ReimbursementProcess(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        data = request.data
        lqd = Liquidation.objects.get(pk=data['id'])
        if lqd.reimbursementStatus == True:
            sweetify.sweetalert(request, icon='warning', title='Liquidation already reimbursed', persistent='Dismiss')
            return JsonResponse(0, safe=False)
        lqd.reimbursementStatus = True
        lqd.save()

        """PUT SOME JOURNAL ENTRIES BELOW THIS"""
        j = Journal()

        j.code = lqd.code
        j.datetimeCreated = datetime.datetime.now()
        j.createdBy = lqd.createdBy
        j.journalDate = datetime.now()
        j.save()
        jeAPI(request, j, 'Credit', dChildAccount.pettyCash, lqd.payable)
        jeAPI(request, j, 'Debit', lqd.createdBy.employeeAccounts.get(name__regex=r"[Pp]ayable"), lqd.payable)
        #### B0SS ####

        """END OF JOURNAL"""
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class ADVDeleteAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        AdvancementThruPettyCash.objects.get(pk=request.data['id']).delete()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class LQDapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'lqds': request.user.branch.liquidation.filter(approved = True),
        }

        return render(request, 'lqd-approved.html', context)

class LQDnonapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'lqds': request.user.branch.liquidation.filter(approved = False),
        }

        return render(request, 'lqd-nonapproved.html', context)

class LiquidationApprovalAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        lqd = Liquidation.objects.get(pk=data['id'])

        ### CODE FOR APPROVING ####
        lqd.approvedBy = request.user
        lqd.approved = True

        j = Journal()

        j.code = lqd.code
        j.datetimeCreated = datetime.datetime.now()
        j.createdBy = lqd.createdBy
        j.journalDate = datetime.date.today()
        j.save()
        request.user.branch.journal.add(j)
        if lqd.advancement:
            ##### PERFECT LIQUIDATION #####
            
            if lqd.change == 0 and lqd.payable == 0:
                print('PERFECT')
                for l in lqd.liquidationentries.all():
                    jeAPI(request, j, 'Debit', l.expense, l.amount)
                jeAPI(request, j, 'Credit', lqd.createdBy.employeeAccounts.get(name__regex=r"[Ad]dvance"), lqd.totalAmount)
                lqd.advancement.balance = 0
                lqd.advancement.closed = True
                lqd.advancement.save()
                lqd.save()

            ##### LIQUIDATION W/ CHANGE #####
            elif lqd.change:
                for l in lqd.liquidationentries.all():
                    jeAPI(request, j, 'Debit', l.expense, l.amount)
                jeAPI(request, j, 'Debit', dChildAccount.pettyCash, lqd.change)
                jeAPI(request, j, 'Credit', lqd.createdBy.employeeAccounts.get(name__regex=r"[Ad]dvance"), lqd.totalAmount + lqd.change)
                lqd.advancement.balance = 0
                lqd.advancement.closed = True
                lqd.advancement.save()
                lqd.save()

            ##### LIQUIDATION W/ PAYABLES #####
            elif lqd.payable:
                print('PAYABLE')
                for l in lqd.liquidationentries.all():
                    jeAPI(request, j, 'Debit', l.expense, l.amount)
                jeAPI(request, j, 'Credit', lqd.createdBy.employeeAccounts.get(name__regex=r"[Ad]dvance"), lqd.advancement.balance)
                try:
                    jeAPI(request, j, 'Credit', lqd.createdBy.employeeAccounts.get(name__regex=r"[Pp]ayable"), lqd.payable)
                except:
                    emploAcc = AccountChild()
                    emploAcc.me = AccountChild.objects.get(name='Payables to Employee')
                    emploAcc.name = 'Payables to Employee - ' + lqd.createdBy.first_name + ' ' + lqd.createdBy.last_name
                    emploAcc.accountSubGroup = request.user.branch.subGroup.get(name="Accounts Payables")
                    emploAcc.amount = Decimal(0)
                    jeAPI(request, j, 'Credit', emploAcc, lqd.payable)
                lqd.advancement.balance = 0
                lqd.advancement.closed = True
                lqd.advancement.save()

        else:
            if not pCashChecker(request, lqd.totalAmount):
                sweetify.sweetalert(request, icon='warning', title='Petty Cash Fund is insufficient!', persistent='Dismiss')
                return JsonResponse(0, safe=False)
                
            for l in lqd.liquidationentries.all():
                jeAPI(request, j, 'Debit', l.expense, l.amount)
            jeAPI(request, j, 'Credit', dChildAccount.pettyCash, lqd.totalAmount)

        notify(request, 'Liquidation approved', lqd.code, '/lqd-approved/', 1)
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class Exportsnonapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        context = {
            'exports': request.user.branch.exports.filter(approved=False),
        }
        return render(request, 'exports-nonapproved.html', context)
    
class Exportsapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        context = {
            'exports': request.user.branch.exports.filter(approved=True),
        }
        return render(request, 'exports-approved.html', context)

class ExportsApprovalAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        data = request.data
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        ex = Exports.objects.get(pk=data['id'])
        ex.approved = True
        ex.approvedBy = request.user
        ex.datetimeApproved = datetime.datetime.now()
        ex.save()

        j = Journal()

        j.code = ex.code
        j.datetimeCreated = ex.datetimeApproved
        j.createdBy = ex.createdBy
        j.journalDate = datetime.datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        totalFees = Decimal(0.0)
        num = 0
        for fees in ex.exportotherfees.all():
            totalFees += fees.fee

        if totalFees != 0.0:
            jeAPI(request, j, 'Credit', dChildAccount.otherIncome, (totalFees*ex.forex))

        for item in ex.exportitemsmerch.all():
            jeAPI(request, j, 'Credit', item.merchInventory.childAccountSales, (item.totalCost*ex.forex)-((ex.discountPeso/ex.exportitemsmerch.all().count())*ex.forex))
        
        jeAPI(request, j, 'Debit', ex.party.accountChild.get(name__regex=r"[Rr]eceivable"), (ex.amountTotal*ex.forex))

        for element in ex.exportitemsmerch.all():
            jeAPI(request, j, 'Credit', element.merchInventory.childAccountInventory, element.merchInventory.purchasingPrice*element.qty)

        for element in ex.exportitemsmerch.all():
            jeAPI(request, j, 'Debit', element.merchInventory.childAccountCostOfSales, element.merchInventory.purchasingPrice*element.qty)

        for item in ex.exportitemsmerch.all():
            element.merchInventory.warehouseitems.all()[0].addQty(-item.qty)
            element.merchInventory.warehouseitems.all()[0].save2()
            
        notify(request, 'Exports approved', ex.code, '/exports-approved/', 1)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
