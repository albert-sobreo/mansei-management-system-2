from rest_framework.views import APIView
from ..models import Holiday, MerchandiseInventory, Warehouse, WarehouseItems
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime

class EMS_HolidaysView(APIView):
    def get(self, request):
        try: 
            year = request.GET['year']
            startDate = '{}-1-1'.format(year)
            endDate = '{}-12-31'.format(year)
        except:
            year = datetime.now().year
            startDate = '{}-1-1'.format(year)
            endDate = '{}-12-31'.format(year)

        context = {
            'holidays': request.user.branch.holiday.filter(date__range=[startDate, endDate]).order_by('date')
        }
        return render(request, 'ems-holidays.html', context)

    def post(self, request):
        holidays = request.data

        for h in holidays:
            holiday = Holiday()

            holiday.date = h['date']
            holiday.year = h['date'].split('-')[0]
            holiday.description = h['description']
            holiday.type = h['type']

            holiday.save()
            request.user.branch.holiday.add(holiday)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_ImportHolidays(APIView):
    def post(self, request):
        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))

        for item in jsonDF:
            h = Holiday()
            if Holiday.objects.filter(date=datetime.fromtimestamp((item['Date'])/1000), description=item['Description']):
                print('Existing')
                continue

            h.date = datetime.fromtimestamp((item['Date'])/1000)
            h.description = item['Description']
            if item['Type'] == 'Special Non-working Holiday':
                h.type = 'sh'
            elif item['Type'] == 'Regular Holiday':
                h.type = 'rh'
            else:
                h.type = 'shw'

            h.save()
            h.year = h.date.year
            h.save()
            request.user.branch.holiday.add(h)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return redirect('/ems-holidays/')

class EMS_SaveEditHoliday(APIView):
    def post(self, request):
        data = request.data
        
        print(data)

        h = Holiday.objects.get(pk=data['id'])
        h.date = data['newDate']
        h.description = data['newDescription']
        print(h.description)
        h.type = data['newType']

        h.save()
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)