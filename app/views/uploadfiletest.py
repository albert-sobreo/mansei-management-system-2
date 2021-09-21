from rest_framework.views import APIView
from app.models import MerchandiseInventory, Warehouse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from ..models import *

class UploadView(View):
    def get(self, request):
        return render(request, 'upload-test-file.html')

    def post(self, request):
        print(request.FILES)

        t = TestUploadFile()
        t.file = request.FILES['file']
        t.save()
        return JsonResponse(0, safe=False)