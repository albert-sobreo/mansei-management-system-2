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

class ADVapproved(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        user = request.user
        context = {
            'advs': user.branch.advancementThruPettyCash.filter(approved = True),
        }
        return render(request, 'adv-approved.html', context)

class ADVnonapproved(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        user = request.user
        context = {
            'advs': user.branch.advancementThruPettyCash.filter(approved = False),
        }
        return render(request, 'adv-nonapproved.html', context)

class ADVapprovalAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
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
        j.journalDate = datetime.now()
        j.save()

        request.user.branch.journal.add(j)

        jeAPI(request, j, 'Credit', dChildAccount.pettyCash, adv.amount)
        try:
            jeAPI(request, j, 'Debit', adv.requestor.employeeAccount.get(name__regex=r"[Pp]ayable"), adv.amount)
        except:
            emploAcc = AccountChild()
            emploAcc.name = 'Account Payables - ' + adv.requestor.first_name + ' ' + adv.requestor.last_name
            emploAcc.accountSubGroup = request.user.branch.subGroup.get(name="Accounts Payables")
            emploAcc.amount = Decimal(0)
            jeAPI(request, j, 'Debit',emploAcc, adv.amount)



        request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.amount -= adv.amount
        request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ReimbursementProcess(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        data = request.data
        lqd = Liquidation.objects.get(pk=data['id'])
        if lqd.reimbursementStatus == True:
            sweetify.sweetalert(request, icon='warning', title='Liquidation already reimbursed', persistent='Dismiss')
            return JsonResponse(0, safe=False)
        lqd.reimbursementStatus = True
        lqd.save()

        """PUT SOME JOURNAL ENTRIES BELOW THIS"""

        #### B0SS ####

        """END OF JOURNAL"""
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class ADVDeleteAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        AdvancementThruPettyCash.objects.get(pk=request.data['id']).delete()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class LQDapproved(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        context = {
            'lqds': request.user.branch.liquidation.filter(approved = True),
        }

        return render(request, 'lqd-approved.html', context)

class LQDnonapproved(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        context = {
            'lqds': request.user.branch.liquidation.filter(approved = False),
        }

        return render(request, 'lqd-nonapproved.html', context)

class LiquidationApprovalAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        data = request.data

        lqd = Liquidation.objects.get(pk=data['id'])

        ### CODE FOR APPROVING ####
        lqd.approvedBy = request.user
        lqd.approved = True

        if lqd.advancement:
            ##### PERFECT LIQUIDATION #####
            if lqd.change == 0 and lqd.payable == 0:
                print('PERFECT')
                lqd.advancement.balance = 0
                lqd.advancement.closed = True
                lqd.advancement.save()
                lqd.save()

            ##### LIQUIDATION W/ CHANGE #####
            elif lqd.change:
                lqd.advancement.balance = 0
                request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.amount += lqd.change
                request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.save()
                lqd.advancement.closed = True
                lqd.advancement.save()
                lqd.save()

            ##### LIQUIDATION W/ PAYABLES #####
            elif lqd.payable:
                print('PAYABLE')
                pass
            
            pass
        else:
            if not pCashChecker(request, lqd.totalAmount):
                sweetify.sweetalert(request, icon='warning', title='Petty Cash Fund is insufficient!', persistent='Dismiss')
                return JsonResponse(0, safe=False)
                
            
            request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.amount -= lqd.totalAmount
            request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.save()

            pass
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)