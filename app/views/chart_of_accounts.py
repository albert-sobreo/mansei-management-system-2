import json
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..models import *
import sweetify

@login_required
def chartOfAccountsView(request):
    return render(request, 'chart_of_accounts.html')

class ChartOfAccountsView(View):
    def get(self, request):
        return render(request, 'chart_of_accounts.html')

class SaveAccountChild(APIView):
    def post(self, request, format=None):
        jsonChild = request.data

        accountChild = AccountChild()

        accountChild.accountSubGroup = AccountSubGroup.objects.get(pk=jsonChild['accountSubGroup'])
        accountChild.code = jsonChild['code']
        accountChild.name = jsonChild['name']
        accountChild.description = jsonChild['description']
        accountChild.contra = jsonChild['contra']
        try:
            accountChild.me = AccountChild.objects.get(pk=jsonChild['me'])
        except Exception as e:
            print(e)

        accountChild.save()

        request.user.branch.accountChild.add(accountChild)

        sweetify.sweetalert(request, icon='success', title='Success!', text='{} has added to {}'.format(accountChild.name, accountChild.accountSubGroup.name), persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SaveAccountGroup(APIView):
    def post(self, request, format=None):
        jsonSubGroup = request.data

        subGroup = AccountSubGroup()

        subGroup.accountGroup = AccountGroup.objects.get(pk=jsonSubGroup['accountGroup'])
        subGroup.code = jsonSubGroup['code']
        subGroup.name = jsonSubGroup['name']
        subGroup.description = jsonSubGroup['description']

        subGroup.save()

        request.user.branch.subGroup.add(subGroup)
        sweetify.sweetalert(request, icon='success', title='Success!', text="{} has added to {}".format(subGroup.name, subGroup.accountGroup.name), persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EditSubGroup(APIView):
    def put(self, request, pk, format = None):
        subGroup = AccountSubGroup.objects.get(pk=pk)
        edit = request.data

        subGroup.code = edit['code']
        subGroup.name = edit['name']
        subGroup.description = edit['description']

        subGroup.save()
        sweetify.sweetalert(request, icon='success', title='Success!',  persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EditChildGroup(APIView):
    def put(self, request, pk, format = None):
        childAccount = AccountChild.object.get(pk=pk)
        edit = request.data

        childAccount.code = edit['code']
        childAccount.name = edit['name']
        childAccount.description = edit['description']
        childAccount.contra = edit['contra']

        try:
            childAccount.me = AccountChild.objects.get(pk=edit['me'])
        except Exception as e:
            print(e)

        childAccount.save()
        sweetify.sweetalert(request, icon='success', title='Success!',  persistent='Dismiss')
        return JsonResponse(0, safe=False)



