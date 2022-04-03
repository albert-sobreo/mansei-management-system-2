from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *
import sweetify
import pandas as pd
import json
from decimal import Decimal
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class ChartOfAccountsView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        return render(request, 'chart_of_accounts.html')

class ChartOfAccountsView2(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        return render(request, 'chart_of_accounts_2.html')

class ImportChartOfAccounts(View):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        df = pd.read_excel(request.FILES['excel'])
        print(df.to_string())
        jsonDF = json.loads(df.to_json(orient='records'))

        existing = []

        for item in jsonDF:
            accGrp = item['Account-Group']
            accSub = item['Account-Sub-Group']
            accChi = item['Account-Child-Group']
            code = item['Code']

            try:
                code = code.split('-')
            except:
                code = ['##', '##', '####']

            branch = request.user.branch

            if branch.accountGroup.filter(name=accGrp):
                print(accGrp + ' already exists')
                accGrp = branch.accountGroup.get(name=accGrp)

            else:
                sweetify.sweetalert(request, icon='error', title='Account Group does not exists.', persistent='Dismiss')
                return JsonResponse(0, safe=False)
            
            if branch.subGroup.filter(name=accSub):
                print(accSub+ ' already exists')
                accSub = branch.subGroup.get(name=accSub)
            else:
                aSub = AccountSubGroup()
                aSub.code = code[1]
                aSub.name = accSub
                aSub.accountGroup = accGrp
                aSub.description = '',
                aSub.amount = Decimal(0)
                aSub.save()
                branch.subGroup.add(aSub)
                accSub = aSub

            if branch.accountChild.filter(name=accChi):
                print(accChi + ' already exists')

            else:
                aChi = AccountChild()
                aChi.code = code[2]
                aChi.name = accChi
                aChi.accountSubGroup = accSub
                aChi.amount = Decimal(0)
                aChi.description = ''
                aChi.save()
                branch.accountChild.add(aChi)

        notify(request, 'New journal accounts has been imported to the system', '', '/chart-of-accounts/', 1)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return redirect('/chart-of-accounts/')



class SaveAccountChild(APIView):
    def post(self, request, format=None):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
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

        notify(request, 'New Journal Account', f'{accountChild.name} has been created', '/chart-of-accounts/', 1)

        sweetify.sweetalert(request, icon='success', title='Success!', text='{} has added to {}'.format(accountChild.name, accountChild.accountSubGroup.name), persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SaveAccountGroup(APIView):
    """ WARNING ::: THIS IS A FUNCTION TO SAVE SUB GROUP NOT ACCOUNT GROUP """
    def post(self, request, format=None):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        jsonSubGroup = request.data

        subGroup = AccountSubGroup()

        subGroup.accountGroup = AccountGroup.objects.get(pk=jsonSubGroup['accountGroup'])
        subGroup.code = jsonSubGroup['code']
        subGroup.name = jsonSubGroup['name']
        subGroup.description = jsonSubGroup['description']

        subGroup.save()

        request.user.branch.subGroup.add(subGroup)

        notify(request, 'New Journal Sub-Group Account', f'{subGroup.name} has been created', '/chart-of-accounts-subgroup//', 1)
        sweetify.sweetalert(request, icon='success', title='Success!', text="{} has added to {}".format(subGroup.name, subGroup.accountGroup.name), persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EditSubGroup(APIView):
    def put(self, request, pk, format = None):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        subGroup = AccountSubGroup.objects.get(pk=pk)
        edit = request.data
        print(request.data)

        subGroup.code = edit['code']
        subGroup.name = edit['name']
        subGroup.description = edit['description']

        subGroup.save()

        notify(request, 'Journal Sub-Group Account Edited', f"{subGroup.name} has been edited", '/chart-of-accounts-subgroup/', 1)
        sweetify.sweetalert(request, icon='success', title='Success!',  persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EditChildGroup(APIView):
    def put(self, request, pk, format = None):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        childAccount = AccountChild.objects.get(pk=pk)
        edit = request.data

        childAccount.code = edit['code']
        childAccount.name = edit['name']
        childAccount.description = edit['description']
        childAccount.contra = edit['contra']

        try:
            childAccount.me = AccountChild.objects.get(pk=edit['me'])
        except Exception as e:
            print(e)

        notify(request, 'Journal Account Edited', f"{childAccount.name} has been edited", '/chart-of-accounts/', 1)
        childAccount.save()
        sweetify.sweetalert(request, icon='success', title='Success!',  persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SubGroupView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        return render(request, 'chart_of_accounts_sub_group.html')

class GroupView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        return render(request, 'chart_of_accounts_group.html')

class EditGroup(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        g = request.data
        group = AccountGroup.objects.get(pk=pk)

        group.code = g['code']
        group.permanence = g['permanence']
        group.normally = g['normally']
        group.save()

        notify(request, 'Journal Group Account Edited', f"{group.name} has been edited", '/chart-of-accounts-group/', 1)

        sweetify.sweetalert(request, icon='success', title='Success!',  persistent='Dismiss')
        return JsonResponse(0, safe=False)

