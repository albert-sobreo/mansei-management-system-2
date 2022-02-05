from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime, date
import re
from time import sleep
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class PPS_ProjectPlannerView(View):
    def get(self, request):
        return render(request, 'pps-planner.html')

class PPS_AddDepartment(APIView):
    def post(self, request):
        data = request.data
        department = ProjectDepartment()
        department.name = data['name']
        department.save()
        request.user.branch.projectDepartment.add(department)

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_AddProject(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        
        project = ProjectPlan()
        project.name = data['name']
        project.dateStart = data['dateStart']
        project.dateEnd = data['dateEnd']
        project.projectLeader = User.objects.get(pk=data['projectLeader'])
        project.department = ProjectDepartment.objects.get(pk=data['department'])
        project.accentColor = data['accentColor']
        project.save()
        request.user.branch.projectPlan.add(project)

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_AddStage(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        stage = ProjectStage()
        stage.name = data['name']
        stage.accentColor = data['accentColor']
        stage.projectPlan = ProjectPlan.objects.get(pk=data['project'])
        stage.save()
        request.user.branch.projectStage.add(stage)

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_AddTask(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        task = ProjectTask()
        task.name = data['name']
        task.datetimeStart = data['datetimeStart']
        task.datetimeEnd = data['datetimeEnd']
        task.notes = data['notes']
        task.projectStage = ProjectStage.objects.get(pk=data['stage'])
        task.save()
        request.user.branch.projectTask.add(task)
        for a in data['assignees']:
            assignee = ProjectAssignee()
            assignee.user = User.objects.get(pk=a['id'])
            assignee.projectTask = task
            assignee.save()
            request.user.branch.projectAssignee.add(assignee)

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_SaveEditStage(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        stage = ProjectStage.objects.get(pk=data['id'])
        stage.name = data['name']
        stage.accentColor = data['accentColor']
        stage.save()

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_DeleteEditStage(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        ProjectStage.objects.get(pk=data['id']).delete()
        
        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_SaveEditTask(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        task = ProjectTask.objects.get(pk=data['id'])
        task.name = data['name']
        task.datetimeStart = data['datetimeStart']
        task.datetimeEnd = data['datetimeEnd']
        task.notes = data['notes']
        for a in task.projectassignee.all():
            a.delete()
        task.save()

        for a in data['assignees']:
            assignee = ProjectAssignee()
            assignee.user = User.objects.get(pk=a['id'])
            assignee.projectTask = task
            assignee.save()
            request.user.branch.projectAssignee.add(assignee)

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_DeleteEditTask(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        ProjectTask.objects.get(pk=data['id']).delete()

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_SaveEditDepartment(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        dep = ProjectDepartment.objects.get(pk=data['id'])
        dep.name = data['name']
        dep.save()

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_SaveEditProject(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data

        print(data)
        
        project = ProjectPlan.objects.get(pk=data['id'])
        project.name = data['name']
        project.dateStart = data['dateStart']
        project.dateEnd = data['dateEnd']
        project.projectLeader = User.objects.get(pk=data['projectLeader'])
        project.department = ProjectDepartment.objects.get(pk=data['department'])
        project.accentColor = data['accentColor']
        project.save()

        sleep(1)
        
        return JsonResponse(0, safe=False)

class PPS_DeleteEditProject(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data
        ProjectPlan.objects.get(pk=data['id']).delete()

        sleep(1)

        return JsonResponse(0, safe=False)

class MoveTaskToStage(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data = request.data

        task = ProjectTask.objects.get(pk=data['taskID'])
        task.projectStage = ProjectStage.objects.get(pk=data['stageID'])
        task.save()

        return JsonResponse(0, safe=False)