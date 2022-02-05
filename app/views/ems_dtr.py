from django.shortcuts import render
from django.views import View
from django.core.exceptions import PermissionDenied

class EMS_MyDTRView(View):
    def get(self, request):
        context = {
            'dtrs': request.user.branch.dtr.filter(user=request.user).order_by('-date')
        }
        return render(request, 'ems-my-dtr.html', context)

class EMS_EmployeeDTRView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'employees': request.user.branch.user.filter(payrollable=True)
        }
        return render(request, 'ems-employee-dtr.html', context)