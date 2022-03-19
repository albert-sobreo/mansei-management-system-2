from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *
import json

class ErrorLoggerAPI(APIView):
    def post(self, request):
        data = request.data

        err = ErrorLogs()

        err.err_message = data['message']
        err.err_url = data['url']
        err.err_line = data['line']
        err.err_datetime = datetime.datetime.now()

        err.save()

        return JsonResponse(0, safe=False)