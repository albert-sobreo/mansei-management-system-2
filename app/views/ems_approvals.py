from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime, date
import re
from .journalAPI import jeAPI
from django.core.exceptions import PermissionDenied

class EMS_OvertimePendingView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        context = {
            'ots': request.user.branch.otRequest.filter(status = "Pending"),
        }
        return render(request, 'ems-overtime-pending.html', context)

class EMS_OvertimeApprovedView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        context = {
            'ots': request.user.branch.otRequest.filter(status = "Approved"),
        }
        return render(request, 'ems-overtime-approved.html', context)

class EMS_OvertimeApproval(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        ot = OTRequest.objects.get(pk=pk)
        ot.datetimeApproved = datetime.now()
        ot.status = "Approved"
        ot.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_OvertimeDisapproval(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        ot = OTRequest.objects.get(pk=pk)
        ot.datetimeApproved = datetime.now()
        ot.status = "Declined"
        ot.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class EMS_UndertimePendingView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        context = {
            'uts': request.user.branch.utRequest.filter(status = "Pending"),
        }
        return render(request, 'ems-undertime-pending.html', context)

class EMS_UndertimeApprovedView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        context = {
            'uts': request.user.branch.utRequest.filter(status = "Approved"),
        }
        return render(request, 'ems-undertime-approved.html', context)

class EMS_UndertimeApproval(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        ut = UTRequest.objects.get(pk=pk)
        ut.datetimeApproved = datetime.now()
        ut.status = "Approved"
        ut.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_UndertimeDisapproval(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        ut = UTRequest.objects.get(pk=pk)
        ut.datetimeApproved = datetime.now()
        ut.status = "Declined"
        ut.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_LeavePendingView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        context = {
            'leaves': request.user.branch.leaveRequest.filter(status = "Pending"),
        }
        return render(request, 'ems-leave-pending.html', context)

class EMS_LeaveApprovedView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        context = {
            'leaves': request.user.branch.leaveRequest.filter(status = "Approved"),
        }
        return render(request, 'ems-leave-approved.html', context)

class EMS_LeaveApproval(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        leave = LeaveRequest.objects.get(pk=pk)

        try: 
            request.user.userleave.all()
            if leave.leaveType == "Vacation Leave":
                if request.user.userleave.vLeave > 0:
                    request.user.userleave.vLeave -= 1
                    request.user.userleave.save()
                else:
                    sweetify.sweetalert(request, icon="error", title="Invalid", text="User doesn't have vacation leave remaining.", persistent="Dismiss")
                    return JsonResponse(0, safe=False)
            elif leave.leaveType == "Sick Leave":
                if request.user.sLeave > 0:
                    request.user.userleave.sLeave -= 1
                    request.user.userleave.save()
                else:
                    sweetify.sweetalert(request, icon="error", title="Invalid", text="User doesn't have sick leave remaining.", persistent="Dismiss")
                    return JsonResponse(0, safe=False)
            # elif leave.leaveType == "Unpaid Leave":
            #     if request.user.uLeave:
            #         request.user.uLeave -= 1
            #     else:
            #         sweetify.sweetalert(request, icon="error", title="Invalid", text="User doesn't have unpaid leave remaining.", persistent="Dismiss")
            #         return JsonResponse(0, safe=False)
            elif leave.leaveType == "SILP":
                if request.user.silp > 0:
                    request.user.userleave.silp -= 1
                    request.user.userleave.save()
                else:
                    sweetify.sweetalert(request, icon="error", title="Invalid", text="User doesn't have SILP remaining.", persistent="Dismiss")
                    return JsonResponse(0, safe=False)
        except Exception as e:
            print(e)
            sweetify.sweetalert(request, icon="error", title="Invalid", text="User's Leave has not been initialized yet. Go to Employees Tab to setup user's leave.", persistent="Dismiss")
            return JsonResponse(0, safe=False)
        leave.approvedBy = request.user
        leave.datetimeApproved = datetime.now()
        leave.status = "Approved"
        leave.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_LeaveDisapproval(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        leave = LeaveRequest.objects.get(pk=pk)
        leave.approvedBy = request.user
        leave.datetimeApproved = datetime.now()
        leave.status = "Declined"
        leave.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_PayrollApprovalAll(APIView):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        y = request.GET['year']
        dateRange = request.GET['dateRange']
        dateStart = dateRange.split(' ')[0]
        dateEnd = dateRange.split(' ')[1]

        salariesExpense = Decimal(0)
        salariesPayable = Decimal(0)
        bonus = Decimal(0)
        deminimis = Decimal(0)
        hdmfER = Decimal(0)
        phicER = Decimal(0)
        sssER = Decimal(0)
        sssPayable = Decimal(0)
        phicPayable = Decimal(0)
        hdmfPayable = Decimal(0)
        withholdingTax = Decimal(0)
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        payrolls = Payroll.objects.filter(branch = request.user.branch, year = y, dateStart = dateStart, dateEnd = dateEnd)

        for payroll in payrolls:
            if payroll.approved:
                continue
            payroll.approved = True
            payroll.approvedBy = request.user
            payroll.dateApproved = date.today()

            salariesExpense += payroll.grossPayBeforeBonus
            salariesPayable += payroll.netPayAfterTaxes
            bonus += (payroll.grossPayAfterBonus - payroll.grossPayBeforeBonus)
            for benefits in payroll.deminimispay.all():
                deminimis += benefits.amount
            hdmfER += payroll.pagibigemployeededuction.amount
            phicER += payroll.phicemployeededuction.er
            sssER += payroll.sssemployeededuction.er
            sssPayable += (payroll.sssemployeededuction.er + payroll.sssemployeededuction.ee)
            phicPayable += (payroll.phicemployeededuction.er + payroll.phicemployeededuction.ee)
            hdmfPayable += (2*payroll.pagibigemployeededuction.amount)
            withholdingTax += payroll.employeetaxdeduction.amount

            j = Journal()

            j.code = 'PYRL' + ": " + str(dateStart) + "  " + str(dateEnd)
            j.datetimeCreated = datetime.now()
            j.createdBy = request.user
            j.journalDate = datetime.now()
            j.save()
            request.user.branch.journal.add(j)
            ########## DEBIT ##########
            # jeAPI(request, j, "Debit", dChildAccount.salariesExpense, salariesExpense)
            # jeAPI(request, j, "Debit", dChildAccount.bonus, bonus)
            # jeAPI(request, j, "Debit", dChildAccount.deminimisBenefit, deminimis)
            # jeAPI(request, j, "Debit", dChildAccount.hdmfShare, hdmfER)
            # jeAPI(request, j, "Debit", dChildAccount.phicERShare, phicER)
            # jeAPI(request, j, "Debit", dChildAccount.sssERShare, sssER)
            ########## CREDIT ##########
            # jeAPI(request, j, "Credit", dChildAccount.salariesPayable, salariesPayable)
            # jeAPI(request, j, "Credit", dChildAccount.sssPayable, sssPayable)
            # jeAPI(request, j, "Credit", dChildAccount.phicPayable, phicPayable)
            # jeAPI(request, j, "Credit", dChildAccount.hdmfPayable, hdmfPayable)
            # jeAPI(request, j, "Credit", dChildAccount.withholdingTaxPayable, withholdingTax)

            payslip = Payslip()
            payslip.payroll = payroll
            payslip.user = payroll.user

            payslip.save()
            request.user.branch.payslip.add(payslip)
            payroll.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return redirect('/ems-payroll/?year={}&period=semi&dateRange={}%20{}'.format(y, dateStart, dateEnd))