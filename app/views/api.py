from decimal import Decimal
from django import views
from django.db.models import query
from django.http.response import Http404
from rest_framework import viewsets
from ..serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status

from ..models import *

from rest_framework.permissions import IsAuthenticated

from datetime import datetime

########## CHART OF ACCOUNTS ##########
class AccountGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountGroupSZ
    queryset = AccountGroup.objects.all().order_by('code')

class AccountChildAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountChildSZ
    queryset = AccountChild.objects.all().order_by('code')

class AccountSubGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubGroupSZ
    queryset = AccountSubGroup.objects.all().order_by('code')

########## CUSTOMER ##########
class CustomerAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartySZ
    queryset = Party.objects.filter(type = 'Customer').order_by('name')

class CustomerTransactionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartyNestedTransactionSZ
    queryset = Party.objects.filter(type = 'Customer').order_by('name')


########## VENDOR ##########
class VendorAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartySZ
    queryset = Party.objects.filter(type = 'Vendor').order_by('name')

class VendorTransactionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartyNestedTransactionSZ
    queryset = Party.objects.filter(type = 'Vendor').order_by('name')

########## WAREHOUSE ##########
class WarehouseAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSZ
    queryset = Warehouse.objects.all()

########## MERCH INVENTORY ##########
class MerchandiseInventoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MerchandiseInventorySZ
    queryset = MerchandiseInventory.objects.all()

########## ACCOUNTING APPROVALS ##########
class PurchaseApprovalNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.filter(approved = False).order_by('datetimeCreated').reverse()

class PurchaseApprovalApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.filter(approved = True).order_by('datetimeCreated').reverse()