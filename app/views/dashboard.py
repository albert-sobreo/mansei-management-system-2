import sweetify
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *

class DashboardView(View):
    def get(self, request):
        context = {
            'branches': Branch.objects.all()
        }
        return render(request, 'dashboard.html', context)

class CreateBranchInDashboard(APIView):
    def post(self, request, format=None):
        branch = request.data

        bdca = BranchDefaultChildAccount()
        bdca.save()

        bp = BranchProfile()
        bp.branchDefaultChildAccount = bdca
        bp.save()

        b = Branch()
        b.name = branch['branchName']
        b.branchProfile = bp
        b.save()

        request.user.branch = b
        request.user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ConnectBranchInDashboard(APIView):
    def post(self, request, format=None):
        branch = request.data

        request.user.branch = Branch.objects.get(pk=branch['branchID'])
        request.user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)