from rest_framework import views
from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime
from django.core.exceptions import PermissionDenied

class EMS_OvertimeRequestsView(APIView):
    def get(self, request):
        return render(request, 'ems-overtime-request.html')

    def post(self, request):
        overTime = request.data
        ot = OTRequest()

        ot.requestedBy = request.user
        ot.hours = overTime['hours']
        ot.date = overTime['date']
        ot.reason = overTime['reason']
        ot.datetimeCreated = datetime.now()
        ot.status = "Pending"
        ot.save()
        request.user.branch.otRequest.add(ot)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_UndertimeRequestsView(APIView):
    def get(self, request):
        return render(request, 'ems-undertime-request.html')

    def post(self, request):
        underTime = request.data
        ut = UTRequest()
        ut.requestedBy = request.user
        ut.timeOut = underTime['timeOut']
        ut.date = underTime['date']
        ut.reason = underTime['reason']
        ut.datetimeCreated = datetime.now()
        ut.status = "Pending"
        ut.save()
        request.user.branch.utRequest.add(ut)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)


class EMS_LeaveRequestsView(APIView):
    def get(self, request):
        return render(request, 'ems-leave-request.html')

    def post(self, request):  
        leave = request.data
        lr = LeaveRequest()
        lr.requestedBy = request.user
        lr.dateStart = leave['dateStart']
        lr.dateEnd = leave['dateEnd']
        lr.reason = leave['reason']
        lr.leaveType = leave['leaveType']
        lr.datetimeCreated = datetime.now()
        lr.status = "Pending"
        lr.save()
        request.user.branch.leaveRequest.add(lr)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_SaveEditLeave(APIView):
    def post(self, request):
        data = request.data

        user = User.objects.get(pk=data['user'])

        try:
            user.userleave
            user.userleave.sLeave = data['sLeave'] if data['sLeave'] >= 0 else 0
            user.userleave.vLeave = data['vLeave'] if data['vLeave'] >= 0 else 0
            user.userleave.silp = data['silp'] if data['silp'] >= 0 else 0
            user.userleave.save()

        except Exception as e:
            print(e)
            userLeave = UserLeave()
            userLeave.user = user
            userLeave.sLeave = data['sLeave'] if data['sLeave'] >= 0 else 0
            userLeave.vLeave = data['vLeave'] if data['vLeave'] >= 0 else 0
            userLeave.silp = data['silp'] if data['silp'] >= 0 else 0
            userLeave.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
