from rest_framework.views import APIView
from app.models import MerchandiseInventory, Warehouse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class WarehouseView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'warehouse.html')


class AddWarehoseAPI(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        print(request.data)
        
        a = Warehouse()

        a.name = request.data['name']
        a.address = request.data['address']
        a.save()
        
        request.user.branch.warehouse.add(a)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
