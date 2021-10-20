from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import datetime, date, timedelta
from decimal import Decimal
import json
import pandas as pd
from dateutil.relativedelta import *


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
        # equipment.deprCycle = request.date['deprCycle']
        equipment.deprCycle = 1
        try:
            equipment.deprRate = Decimal(Decimal(equipment.purchasePrice)*equipment.deprCycle)/(int(equipment.usefulLife)*12)
        except Exception as e:
            print(e)
            sweetify.sweetalert(request, icon='error', title='Error!', text="Purchasing Price and Useful Life are required to calculate Depr. rate.", persistent='Dismiss')
            return JsonResponse(0, safe=False)

        pDate = (equipment.purchaseDate).split('-')
        equipment.startingDeprDate = date(int(pDate[0]), int(pDate[1]), 1)
        
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
            equipment.deprCycle = item['Depreciation-Cycle']
            # equipment.startingDeprDate
            equipment.deprRate = (equipment.purchasePrice*equipment.deprCycle)/(12*equipment.usefulLife)

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

class LapsingView(View):
    def get(self, request):
        return render(request, 'ppe-lapsing-schedule.html')

class UpdateDepr(View):
    def get(self, request):
        ppes = request.user.branch.ppe.all()

        currentDate = date.today()

        for ppe in ppes:
            if ppe.usefulLife != None:
                if ppe.ppehistoryofdepr.all():
                    print('IN TRY')
                    latestDepr = ppe.ppehistoryofdepr.latest('pk')
                    totalMonths = (12 * relativedelta(currentDate, latestDepr.date).years) + relativedelta(currentDate, latestDepr.date).months
                    print(totalMonths)
                    if totalMonths >= ppe.deprCycle:
                        if currentDate.day >= latestDepr.date.day:
                            deprAmount = totalMonths * ppe.deprRate
                            ppe.bookValue -= deprAmount
                            ppe.accumDepr += deprAmount

                            deprHistory = PPEHistoryOfDepr()
                            deprHistory.ppe = ppe
                            deprHistory.date = date(currentDate.year, currentDate.month, 1)
                            deprHistory.deprAmount = deprAmount
                            deprHistory.bookValue = ppe.bookValue
                            deprHistory.accumDeprAmount = ppe.accumDepr

                            ppe.save()
                            deprHistory.save()

                else:
                    totalMonths = 12 * relativedelta(currentDate, ppe.startingDeprDate).years + relativedelta(currentDate, ppe.startingDeprDate).months
                    if totalMonths >= ppe.deprCycle:
                    # if (currentDate.month - ppe.startingDeprDate.month) >= ppe.deprCycle:
                        if currentDate.day >= ppe.startingDeprDate.day:
                            deprAmount = totalMonths * ppe.deprRate
                            ppe.bookValue -= deprAmount
                            ppe.accumDepr += deprAmount

                            deprHistory = PPEHistoryOfDepr()
                            deprHistory.ppe = ppe
                            deprHistory.date = date(currentDate.year, currentDate.month, 1)
                            deprHistory.deprAmount = deprAmount
                            deprHistory.bookValue = ppe.bookValue
                            deprHistory.accumDeprAmount = ppe.accumDepr

                            ppe.save()
                            deprHistory.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return redirect('/ppe-lapsing-schedule/')