from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
import pandas as pd
import json
from django.core.exceptions import PermissionDenied

class NotificationReceiver(APIView):
    def get(self, request, pk):
        noti = Notifications.objects.get(pk=pk)
        noti.read = True
        noti.save()

        return JsonResponse(noti.url, safe=0)

class NotificationUnreadChecker(APIView):
    def get(self, request):
        noti = request.user.notifications.filter(read=False)
        data = False if noti.count() == 0 else True
        return JsonResponse(data, safe=False)