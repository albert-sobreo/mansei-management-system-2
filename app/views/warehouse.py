from rest_framework.views import APIView
from app.models import MerchandiseInventory, Warehouse
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
import sweetify

class WarehouseView(View):
    def get(self, request, format=None):
        return render(request, 'warehouse.html')


class AddWarehoseAPI(APIView):
    def post(self, request, format = None):
        print(request.data)
        
        a = Warehouse()

        a.name = request.data['name']
        a.address = request.data['address']
        a.save()
        
        request.user.branch.warehouse.add(a)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)