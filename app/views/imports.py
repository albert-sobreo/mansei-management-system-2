import json
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from ..serializers import *
from ..models import *
import sweetify
import pandas as pd

class ImportATC(View):
    def post(self, request, format=None):
        df = pd.read_excel(request.FILES['excel'])
        jsonDF = json.loads(df.to_json(orient='records'))

        for jsonATC in jsonDF:
            atc = ATC()

            if ATC.objects.filter(code=jsonATC['code'], rate=jsonATC['rate'], description=jsonATC['description']):
                print(jsonATC['code'] + ' exists')
                continue
            atc.code = jsonATC['code']
            atc.rate = jsonATC['rate']
            atc.description = jsonATC['description']
            atc.save()
        
        sweetify.sweetalert(request, icon="success", title="Success!", persistent="Dismiss")
        return redirect('/purchase-order/')