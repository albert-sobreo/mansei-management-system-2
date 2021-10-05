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

class EMS_OvertimePendingView(View):
    def get(self, request):

        context = {
            'ots': request.user.branch.otRequest.filter(status = "Pending"),
        }
        return render(request, 'ems-overtime-pending.html', context)

class EMS_OvertimeApprovedView(View):
    def get(self, request):

        context = {
            'ots': request.user.branch.otRequest.filter(status = "Approved"),
        }
        return render(request, 'ems-overtime-approved.html', context)

class EMS_OvertimeApproval(APIView):
    def put(self, request, pk):
        ot = OTRequest.objects.get(pk=pk)
        ot.datetimeApproved = datetime.now()
        ot.status = "Approved"
        ot.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_OvertimeDisapproval(APIView):
    def put(self, request, pk):
        ot = OTRequest.objects.get(pk=pk)
        ot.datetimeApproved = datetime.now()
        ot.status = "Declined"
        ot.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class EMS_UndertimePendingView(View):
    def get(self, request):

        context = {
            'uts': request.user.branch.utRequest.filter(status = "Pending"),
        }
        return render(request, 'ems-undertime-pending.html', context)

class EMS_UndertimeApprovedView(View):
    def get(self, request):

        context = {
            'uts': request.user.branch.utRequest.filter(status = "Approved"),
        }
        return render(request, 'ems-undertime-approved.html', context)

class EMS_UndertimeApproval(APIView):
    def put(self, request, pk):
        ut = UTRequest.objects.get(pk=pk)
        ut.datetimeApproved = datetime.now()
        ut.status = "Approved"
        ut.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_UndertimeDisapproval(APIView):
    def put(self, request, pk):
        ut = UTRequest.objects.get(pk=pk)
        ut.datetimeApproved = datetime.now()
        ut.status = "Declined"
        ut.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_LeavePendingView(View):
    def get(self, request):

        context = {
            'leaves': request.user.branch.leaveRequest.filter(status = "Pending"),
        }
        return render(request, 'ems-leave-pending.html', context)

class EMS_LeaveApprovedView(View):
    def get(self, request):

        context = {
            'leaves': request.user.branch.leaveRequest.filter(status = "Approved"),
        }
        return render(request, 'ems-leave-approved.html', context)

class EMS_LeaveApproval(APIView):
    def put(self, request, pk):
        leave = LeaveRequest.objects.get(pk=pk)
        leave.approvedBy = request.user
        leave.datetimeApproved = datetime.now()
        leave.status = "Approved"
        leave.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_LeaveDisapproval(APIView):
    def put(self, request, pk):
        leave = LeaveRequest.objects.get(pk=pk)
        leave.approvedBy = request.user
        leave.datetimeApproved = datetime.now()
        leave.status = "Declined"
        leave.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)