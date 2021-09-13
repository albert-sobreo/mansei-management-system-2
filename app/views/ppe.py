from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from datetime import datetime
from decimal import Decimal
import json
import pandas as pd


class PPEView(View):
    def get(self, request):
        return render(request, 'ppe.html')

class AddPPE(APIView):
    def post(self, request, format = None):

        equipment = PPE()
        equipment.code = request.data['code']
        equipment.name = request.data['name']
        equipment.type = request.data['type']
        equipment.purchasePrice = request.data['purchasePrice']
        equipment.purchaseDate = request.data['purchaseDate']
        equipment.accumDepr = request.data['accumDepr']
        equipment.bookValue = request.data['bookValue']
        equipment.usefulLife = request.data['usefulLife']
        
        equipment.save()
        request.user.branch.ppe.add(equipment)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ImportPPE(View):
    def post(self, request, format = None):
        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))

        for item in jsonDF:
            equipment = PPE()

            if PPE.objects.filter(code=item['Code']):
                print('it exists')
                continue

            equipment.code = item['Code']
            equipment.name = item['Name']
            equipment.type = item['Type']
            equipment.purchaseDate = datetime.fromtimestamp((item['Purchase-Date'])/1000)

            item['Book-Value'] = str(item['Book-Value']).replace('₱', '')
            item['Book-Value'] = item['Book-Value'].replace(',', '')
            equipment.bookValue = item['Book-Value']

            item['Purchase-Price'] = str(item['Purchase-Price']).replace('₱', '')
            item['Purchase-Price'] = item['Purchase-Price'].replace(',', '')
            equipment.purchasePrice = item['Purchase-Price']

            item['Accum-Depr'] = str(item['Accum-Depr']).replace('₱', '')
            item['Accum-Depr'] = item['Accum-Depr'].replace(',', '')
            equipment.accumDepr = item['Accum-Depr']

            equipment.usefulLife = item['Useful-Life']

            equipment.save()
            request.user.branch.ppe.add(equipment)

        sweetify.sweetalert(request, icon="success", title="Success!", persistent="Dismiss")
        return redirect('/ppe/')

class EditPPE(APIView):
    def put(self, request, pk, format = None):

        equipment = PPE.objects.get(pk=pk)

        edit = request.data

        equipment.code = edit['code']
        equipment.name = edit['name']
        equipment.type = edit['type']
        equipment.purchaseDate = edit['purchaseDate']
        equipment.purchasePrice = edit['purchasePrice']
        equipment.bookValue = edit['bookValue']
        equipment.usefulLife = edit['usefulLife']
        equipment.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
