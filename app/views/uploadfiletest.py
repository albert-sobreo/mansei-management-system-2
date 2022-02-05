from rest_framework.views import APIView
from app.models import MerchandiseInventory, Warehouse
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from ..models import *
from .notificationCreate import *

class UploadView(View):
    def get(self, request):
        return render(request, 'upload-test-file.html')

    def post(self, request):
        print(request.FILES)

        t = TestUploadFile()
        t.file = request.FILES['file']
        t.save()
        return JsonResponse(0, safe=False)

import io
import xlsxwriter

class ExcelReportAPI(View):
    def get(self, request):
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Some Data')
        worksheet.write(0, 1, 'Some Data 2')
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.xlsx')