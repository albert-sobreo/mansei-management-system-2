from rest_framework.views import APIView
from ..models import MerchandiseInventory, Warehouse, WarehouseItems
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime, date
from ..models import*
from .notificationCreate import *

class MyProfileView(View):
    def get(self, request):
        return render(request, 'my-profile.html')

class MyProfileSaveProfilePicture(View):
    def post(self, request):

        request.user.image.delete(save=False)
        request.user.image = request.FILES['profilePicture']
        request.user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class MyProfileSavePersonalInfo(APIView):
    def post(self, request):
        d = request.data
        
        u = request.user

        u.first_name = d['first_name']
        u.last_name = d['last_name']
        u.address = d['address']
        u.mobile = d['mobile']
        u.dob = d['dob']
        u.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class MyProfileSaveEmployeeInfo(APIView):
    def post(self, request):
        d = request.data
        u = request.user

        u.idUser = d['idUser']
        u.tin = d['tin']
        u.sss = d['sss']
        u.phic = d['phic']
        u.hdmf = d['hdmf']

        u.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class MyProfileSavePassword(APIView):
    def post(self, request):
        d = request.data
        u = request.user

        u.set_password(d['password'])
        u.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class MyProfileSaveEmail(APIView):
    def post(self, request):
        d = request.data
        u = request.user

        u.email = d['email']
        u.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)