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





########## PURCHASE ORDER ##########
class PurchaseOrderAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.all()

class PurchaseOrderApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.filter(approved=True)





########## SALES CONTRACT ##########
class SalesContractAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesContractNestedSZ
    queryset = SalesContract.objects.all()





########## ACCOUNTING APPROVALS ##########
class PurchaseApprovalNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.filter(approved = False).order_by('datetimeCreated').reverse()

class PurchaseApprovalApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.filter(approved = True).order_by('datetimeCreated').reverse()

class SalesContractApprovalNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesContractNestedSZ
    queryset = SalesContract.objects.filter(approved = False)

class SalesContractApprovalApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesContractNestedSZ
    queryset = SalesContract.objects.filter(approved = True)





########## SPECIAL TRUCK ##########
class SpecialTruckAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SpecialTruckSZ
    queryset = Deliveries.objects.all()





########## LEDGER ##########
class LedgerAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LedgerSZ
    queryset = AccountChild.objects.all().order_by('pk')





########## DELIVERY ##########
class DeliveriesAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveriesSZ
    queryset = Deliveries.objects.all()






########## ATC ##########
class ATCAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ATCSZ
    queryset = ATC.objects.all()






########## PURCHASE REQUEST ##########
class PurchaseRequestAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestSZ
    queryset = PurchaseRequest.objects.all()

class PurchaseRequestApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestSZ
    queryset = PurchaseRequest.objects.filter(approved=True)

class PurchaseRequestNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestSZ
    queryset = PurchaseRequest.objects.filter(approved=False)


class PurchaseRequestNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestNestedSZ
    queryset = PurchaseRequest.objects.all()





########## RECEIVING REPORT ##########

class ReceivingReportNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivingReportNestedSZ
    queryset = ReceivingReport.objects.all()






########## INWARD INVENTORY ##########

class InwardInventoryNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InwardInventoryNestedSZ
    queryset = InwardInventory.objects.all()


########## PAYMENT VOUCHER ##########

class PaymentVoucherAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VoucherSZ
    queryset = PaymentVoucher.objects.all()




########## QUOTATIONS ##########

class QuotationsAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuotationsSZ
    queryset = Quotations.objects.all()





########### SALES ORDER ##########
class SalesOrderAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesOrderNestedSZ
    queryset = SalesOrder.objects.all()





########## SALES CONTRACT ##########
class SalesContractAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesContractSZ
    queryset = SalesContract.objects.all()





########### BranchDefaultChildAccount ##########
class BranchDefaultChildAccountAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchDefaultChildAccountSZ
    queryset = BranchDefaultChildAccount.objects.all()