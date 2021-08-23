from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *

class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')