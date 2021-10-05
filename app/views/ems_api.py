from django.db.models import query
from django.http.response import Http404, JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import CurrentUserDefault

class OTRequestAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OTRequestSZ
    queryset = OTRequest.objects.all()

class UTRequestAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UTRequestSZ
    queryset = UTRequest.objects.all()