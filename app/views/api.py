from django.db.models import query
from django.http.response import Http404, JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.serializers import Serializer
from ..serializers import *
from rest_framework.views import APIView
from ..models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from rest_framework.decorators import action

########## CHART OF ACCOUNTS ##########
class AccountGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountGroupSZ
    queryset = AccountGroup.objects.all().order_by('code')






class AccountChildAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountChildSZ
    queryset = AccountChild.objects.all().order_by('code')


class AccountChildNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountChildNestedSZ
    queryset = AccountChild.objects.all()

class AccountSubGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubGroupSZ
    queryset = AccountSubGroup.objects.all().order_by('code')






class GetAccountExpensesAPI(APIView):
    def get(self, request, format=None):
        lst = []
        expGroup = request.user.branch.accountGroup.filter(name__regex=r'[Ee]xpense')
        for exp in expGroup:
            for sub in exp.accountsubgroup.all():
                for child in sub.accountchild.all():
                    lst.append([child.pk, child.name])
        return JsonResponse(lst, safe=False)






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

class WarehouseNestedAPI(viewsets.ModelViewSet):
    permissions = [IsAuthenticated]
    serializer_class = WarehouseNestedSZ
    queryset = Warehouse.objects.all()






########## MERCH INVENTORY ##########
class MerchandiseInventoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MerchandiseInventorySZ
    queryset = MerchandiseInventory.objects.all()

class MerchandiseInventoryNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MerchandiseInventoryNestedSZ
    queryset = MerchandiseInventory.objects.all()





########## OTHER INVENTORY ##########
class OtherInventoryAPI2(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OtherInventorySZ
    queryset = OtherInventory.objects.all()

class OtherInventoryAPI(APIView):
    def post(self, request, format=None):
        try:
            item = OtherInventory.objects.get(name=request.data['name'])
            return JsonResponse (item.qty, safe=False)
        except:
            # otherInv = OtherInventory
            # otherInv.name = request.data['name']
            # otherInv.qty = 0
            # otherInv.purchasingPrice = Decimal(0.0)
            # otherInv.save()

            # item = otherInv
            return JsonResponse(0, safe=False)
        





########## PURCHASE ORDER ##########
class PurchaseOrderAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.all()

class PurchaseOrderApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    queryset = PurchaseOrder.objects.filter(approved=True)

class PurchaseOrderApprovedRepairAPI(APIView):
    def get(self, request, format=None):
        lst = []
        repairAccount = request.user.branch.branchProfile.branchDefaultChildAccount.rm
        poRepairOnly = request.user.branch.purchaseOrder.filter(poitemsother__type = repairAccount.id)
        serializer = PurchaseOrderNestedSZ(poRepairOnly, many=True)
        return JsonResponse(serializer.data, safe=False)






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

class ReceivingReportNestedApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivingReportNestedSZ
    queryset = ReceivingReport.objects.filter(approved=True).order_by("-pk")






########## INWARD INVENTORY ##########
class InwardInventoryNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InwardInventoryNestedSZ
    queryset = InwardInventory.objects.all()

class InwardInventoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InwardInventorySZ
    queryset = InwardInventory.objects.all()






########## PAYMENT VOUCHER ##########
class PaymentVoucherAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VoucherSZ
    queryset = PaymentVoucher.objects.all()




########## RECEIVED PAYMENTS ##########
class ReceivedPaymentAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivedPaymentsSZ
    queryset = ReceivePayment.objects.all()





########## INVOICE ##########
class SalesInvoiceAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesInvoiceSZ
    queryset = SalesInvoice.objects.all()





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

########### TRANSFER & ADJUSTMENTS ##########
class TransferAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSZ
    queryset = Transfer.objects.all()

class AdjustmentAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AdjustmentSZ
    queryset = Adjustments.objects.all()





########### BranchDefaultChildAccount ##########
class BranchDefaultChildAccountAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchDefaultChildAccountSZ
    queryset = BranchDefaultChildAccount.objects.all()





########## USER WITH DTR ##########
class UserWithDTRAPI(viewsets.ModelViewSet):
    serializer_class = UserWithDTRSZ
    queryset = User.objects.all()





########## JUST USER ##########
class UserAPI(viewsets.ModelViewSet):
    serializer_class = UserNestedSZ
    queryset = User.objects.all()


class UserAPI2(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNameOnlySZ
    queryset = User.objects.all()

class UserPayrollableAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNameOnlySZ
    queryset = User.objects.filter(payrollable=True)

    @action(detail=False, methods=['get'])
    def filterByBranch(self, request):
        queryset = User.objects.filter(branch=request.user.branch, payrollable=True)
        serializer = UserNameOnlySZ(queryset, many=True)
        return Response(serializer.data)

class UserWith13thAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWith13thSZ
    queryset = User.objects.all()





########## PPE ##########
class PPENestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PPENestedSZ
    queryset = PPE.objects.all()

class PPEAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PPESZ
    queryset = PPE.objects.all()





########## CR ##########
class CRNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CRNestedSZ
    queryset = CompletionReport.objects.all()




########## PAYROLL ##########
class ComplexPayrollAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplexPayrollSZ
    queryset = Payroll.objects.all()

class PayrollAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PayrollSZ
    queryset = Payroll.objects.all()





########## DE MINIMIS ##########
class DeMinimisAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeMinimisSZ
    queryset = DeMinimis.objects.all()





########## HOLIDAY ##########
class HolidayAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HolidaySZ
    queryset = Holiday.objects.all()





########## PROJECT PLANNING ##########
class ProjectAssigneeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectAssigneeSZ
    queryset = ProjectAssignee.objects.all()

class ProjectTaskAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectTaskSZ
    queryset = ProjectTask.objects.all()

class ProjectTaskNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectTaskNestedSZ
    queryset = ProjectTask.objects.all()

class ProjectStageAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectStageSZ
    queryset = ProjectStage.objects.all()

class ProjectStageNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectStageNestedSZ
    queryset = ProjectStage.objects.all()

class ProjectPlanAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectPlanSZ
    queryset = ProjectPlan.objects.all()

class ProjectPlanNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectPlanNestedSZ
    queryset = ProjectPlan.objects.all()

class ProjectDepartmentAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectDepartmentSZ
    queryset = ProjectDepartment.objects.all()

    @action(detail=False, methods=['get'])
    def filterByBranch(self, request):
        queryset = ProjectDepartment.objects.filter(branch=request.user.branch)
        serializer = ProjectDepartmentSZ(queryset, many=True)
        return Response(serializer.data)

class ProjectDepartmentNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectDepartmentNestedSZ
    queryset = ProjectDepartment.objects.all()

    @action(detail=False, methods=['get'])
    def filterByBranch(self, request):
        queryset = ProjectDepartment.objects.filter(branch=request.user.branch)
        serializer = ProjectDepartmentNestedSZ(queryset, many=True)
        return Response(serializer.data)

class AssigneeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def filterByBranch(self, request):
        queryset = User.objects.filter(branch=request.user.branch)
        serializer = UserNameOnlySZ(queryset, many=True)
        return Response(serializer.data)

class TotalBonusOfUserForCurrentYearAPI(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.get(pk=data['user'])

        payroll = user.payroll.filter(year=data['year'])

        totalBonusAmount = 0

        for pay in payroll: 
            for bonus in pay.bonuspay.all():
                totalBonusAmount += bonus.amount

        print(totalBonusAmount)
        return JsonResponse(totalBonusAmount, safe=False)

class DashboardAPI(APIView):
    def get(self, request):
        data = request.data
        serializer = UserDashboardSZ(request.user)

        # dashData = {
        #     "branchName": request.user.branch.name,
        #     "merchAmount": request.user.branch.branchProfile.branchDefaultChildAccount.merchInventory.amount,
        #     "salesAmount": request.user.branch.branchProfile.branchDefaultChildAccount.sales.amount,
        #     "revAmount": request.user.branch.accountGroup.get(name__regex=r'[Rr]evenue').amount,
        #     'user': serializer.data
        # }

        dashData = {}

        try:
            dashData['branchName'] = request.user.branch.name
        except:
            dashData['branchName'] = "Null"
        
        try:
            dashData['merchAmount'] = request.user.branch.branchProfile.branchDefaultChildAccount.merchInventory.amount
        except:
            dashData['merchAmount'] = 0

        try:
            dashData["salesAmount"] = request.user.branch.branchProfile.branchDefaultChildAccount.sales.amount
        except:
            dashData["salesAmount"] = 0

        try:
            dashData["revAmount"] = request.user.branch.accountGroup.get(name__regex=r'[Rr]evenue').amount
        except:
            dashData["revAmount"] = 0

        try:
            dashData["user"] = serializer.data
        except Exception as e:
            print(e)
            dashData['user'] = None

        try:
            serializer = AnnouncementSZ(request.user.branch.branchannouncement, many=True)
            dashData["announcements"] = serializer.data
        except:
            dashData["announcements"] = []

        return JsonResponse(dashData, safe=False)

########## PETTY CASH ###########
class AdvancementAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AdvancementSZ
    queryset = AdvancementThruPettyCash.objects.all()



########## BRANCH ##########
class BranchListAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSZ
    queryset = Branch.objects.all()