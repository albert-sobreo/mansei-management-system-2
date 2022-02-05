from curses import echo
import datetime
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
from decimal import Decimal
import re
from .notificationCreate import *

########## NOTIFICATIONS ##########
class NotificationsAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationsSZ

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-pk')







########## CHART OF ACCOUNTS ##########
class AccountGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountGroupSZ

    def get_queryset(self):
        return self.request.user.branch.accountGroup.all()

class AccountChildAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountChildSZ

    def get_queryset(self):
        return self.request.user.branch.accountChild.all()


class AccountChildNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountChildNestedSZ

    def get_queryset(self):
        return self.request.user.branch.accountChild.all()

class AccountSubGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubGroupSZ

    def get_queryset(self):
        return self.request.user.branch.subGroup.all()






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

    def get_queryset(self):
        return self.request.user.branch.party.filter(type = 'Customer').order_by('name')

class CustomerTransactionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartyNestedTransactionSZ

    def get_queryset(self):
        return self.request.user.branch.party.filter(type = 'Customer').order_by('name')






########## VENDOR ##########
class VendorAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartySZ

    def get_queryset(self):
        return self.request.user.branch.party.filter(type = 'Vendor').order_by('name')

class VendorTransactionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PartyNestedTransactionSZ

    def get_queryset(self):
        return self.request.user.branch.party.filter(type = 'Vendor').order_by('name')






########## WAREHOUSE ##########
class WarehouseAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSZ

    def get_queryset(self):
        return self.request.user.branch.warehouse.all()


class WarehouseNestedAPI(viewsets.ModelViewSet):
    permissions = [IsAuthenticated]
    serializer_class = WarehouseNestedSZ

    def get_queryset(self):
        return self.request.user.branch.warehouse.all()







########## MERCH INVENTORY ##########
class MerchandiseInventoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MerchandiseInventorySZ

    def get_queryset(self):
        return self.request.user.branch.merchInventory.all()

class MerchandiseInventoryNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MerchandiseInventoryNestedSZ
    
    def get_queryset(self):
        return self.request.user.branch.merchInventory.all()





########## OTHER INVENTORY ##########
class OtherInventoryAPI2(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OtherInventorySZ

    def get_queryset(self):
        return self.request.user.branch.otherInventory.all()


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

    def get_queryset(self):
        return self.request.user.branch.purchaseOrder.all()


class PurchaseOrderApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ

    def get_queryset(self):
        return self.request.user.branch.purchaseOrder.filter(approved=True)


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

    def get_queryset(self):
        return self.request.user.branch.salesContract.all()



########## EXPORTS ##########
class ExportsAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExportNestedSZ

    def get_queryset(self):
        return self.request.user.branch.exports.all()





########## ACCOUNTING APPROVALS ##########
class PurchaseApprovalNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ
    
    def get_queryset(self):
        return self.request.user.branch.purchaseOrder.filter(approved = False).order_by('datetimeCreated').reverse()

class PurchaseApprovalApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderNestedSZ

    def get_queryset(self):
        return self.request.user.branch.purchaseOrder.filter(approved = True).order_by('datetimeCreated').reverse()


class SalesContractApprovalNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesContractNestedSZ

    def get_queryset(self):
        return self.request.user.branch.salesContract.filter(approved = False)

class SalesContractApprovalApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesContractNestedSZ

    def get_queryset(self):
        return self.request.user.branch.salesContract.filter(approved = True)





########## SPECIAL TRUCK ##########
class SpecialTruckAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SpecialTruckSZ

    def get_queryset(self):
        return self.request.user.branch.deliveries.all()





########## LEDGER ##########
class LedgerAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LedgerSZ

    def get_queryset(self):
        return self.request.user.branch.accountChild.all().order_by('pk')





########## DELIVERY ##########
class DeliveriesAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveriesSZ

    def get_queryset(self):
        return self.request.user.branch.accountChild.all()






########## ATC ##########
class ATCAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ATCSZ
    queryset = ATC.objects.all()



########## PURCHASE REQUEST ##########
class PurchaseRequestAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestSZ

    def get_queryset(self):
        return self.request.user.branch.purchaseRequest.all()

class PurchaseRequestApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestSZ

    def get_queryset(self):
        return self.request.user.branch.purchaseRequest.filter(approved=True)

class PurchaseRequestNonApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestSZ

    def get_queryset(self):
        return self.request.user.branch.purchaseRequest.filter(approved=False)


class PurchaseRequestNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseRequestNestedSZ

    def get_queryset(self):
        return self.request.user.branch.purchaseRequest.all()





########## RECEIVING REPORT ##########
class ReceivingReportNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivingReportNestedSZ
    def get_queryset(self):
        return self.request.user.branch.receivingReport.all()

class ReceivingReportNestedApprovedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivingReportNestedSZ

    def get_queryset(self):
        return self.request.user.branch.receivingReport.filter(approved=True).order_by("-pk")






########## INWARD INVENTORY ##########
class InwardInventoryNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InwardInventoryNestedSZ
    def get_queryset(self):
        return self.request.user.branch.inwardInventory.all()

class InwardInventoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InwardInventorySZ
    def get_queryset(self):
        return self.request.user.branch.inwardInventory.all()






########## PAYMENT VOUCHER ##########
class PaymentVoucherAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VoucherSZ
    def get_queryset(self):
        return self.request.user.branch.paymentVoucher.all()




########## RECEIVED PAYMENTS ##########
class ReceivedPaymentAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivedPaymentsSZ
    def get_queryset(self):
        return self.request.user.branch.receivePayment.all()





########## INVOICE ##########
class SalesInvoiceAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesInvoiceSZ
    def get_queryset(self):
        return self.request.user.branch.receivePayment.all()





########## QUOTATIONS ##########
class QuotationsAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuotationsSZ
    def get_queryset(self):
        return self.request.user.branch.quotations.all()





########### SALES ORDER ##########
class SalesOrderAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesOrderNestedSZ
    def get_queryset(self):
        return self.request.user.branch.salesOrder.all()

########### TRANSFER & ADJUSTMENTS ##########
class TransferAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSZ
    def get_queryset(self):
        return self.request.user.branch.transfer.all()

class AdjustmentAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AdjustmentSZ
    def get_queryset(self):
        return self.request.user.branch.adjustments.all()





########### BranchDefaultChildAccount ##########
class BranchDefaultChildAccountAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchDefaultChildAccountSZ
    queryset = BranchDefaultChildAccount.objects.all()

    """DOESNT NEED GET_QUERYSET"""





########## USER WITH DTR ##########
class UserWithDTRAPI(viewsets.ModelViewSet):
    serializer_class = UserWithDTRSZ
    def get_queryset(self):
        return self.request.user.branch.user.all()





########## JUST USER ##########
class UserAPI(viewsets.ModelViewSet):
    serializer_class = UserNestedSZ
    def get_queryset(self):
        return self.request.user.branch.user.all()


class UserAPI2(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNameOnlySZ
    def get_queryset(self):
        return self.request.user.branch.user.all()

class UserPayrollableAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNameOnlySZ
    queryset = User.objects.filter(payrollable=True)

    """DOESNT NEED GET_QUERYSET"""

    @action(detail=False, methods=['get'])
    def filterByBranch(self, request):
        queryset = User.objects.filter(branch=request.user.branch, payrollable=True)
        serializer = UserNameOnlySZ(queryset, many=True)
        return Response(serializer.data)

class UserWith13thAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWith13thSZ
    def get_queryset(self):
        return self.request.user.branch.user.all()





########## PPE ##########
class PPENestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PPENestedSZ
    def get_queryset(self):
        return self.request.user.branch.ppe.all()

class PPEAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PPESZ
    def get_queryset(self):
        return self.request.user.branch.ppe.all()





########## CR ##########
class CRNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CRNestedSZ
    def get_queryset(self):
        return self.request.user.branch.completionReport.all()




########## PAYROLL ##########
class ComplexPayrollAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplexPayrollSZ
    def get_queryset(self):
        return self.request.user.branch.payroll.all()

class PayrollAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PayrollSZ
    def get_queryset(self):
        return self.request.user.branch.payroll.all()





########## DE MINIMIS ##########
class DeMinimisAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeMinimisSZ
    def get_queryset(self):
        return self.request.user.branch.deMinimis.all()





########## HOLIDAY ##########
class HolidayAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HolidaySZ
    def get_queryset(self):
        return self.request.user.branch.holiday.all()





########## PROJECT PLANNING ##########
class ProjectAssigneeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectAssigneeSZ
    def get_queryset(self):
        return self.request.user.branch.projectAssignee.all()

class ProjectTaskAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectTaskSZ
    def get_queryset(self):
        return self.request.user.branch.projectTask.all()

class ProjectTaskNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectTaskNestedSZ
    def get_queryset(self):
        return self.request.user.branch.projectTask.all()

class ProjectStageAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectStageSZ
    def get_queryset(self):
        return self.request.user.branch.projectStage.all()

class ProjectStageNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectStageNestedSZ

    def get_queryset(self):
        return self.request.user.branch.projectStage.all()

class ProjectPlanAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectPlanSZ

    def get_queryset(self):
        return self.request.user.branch.projectPlan.all()

class ProjectPlanNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectPlanNestedSZ

    def get_queryset(self):
        return self.request.user.branch.projectPlan.all()

class ProjectDepartmentAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectDepartmentSZ
    queryset = ProjectDepartment.objects.all()

    """DOESNT NEED GET_QUERYSET"""

    @action(detail=False, methods=['get'])
    def filterByBranch(self, request):
        queryset = ProjectDepartment.objects.filter(branch=request.user.branch)
        serializer = ProjectDepartmentSZ(queryset, many=True)
        return Response(serializer.data)

class ProjectDepartmentNestedAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectDepartmentNestedSZ
    queryset = ProjectDepartment.objects.all()

    """DOESNT NEED GET_QUERYSET"""

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
        except Exception as e:
            print('Branch Name Exception:', e)
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

        try:
            dashData['pettyCash'] = request.user.branch.branchProfile.branchDefaultChildAccount.pettyCash.amount
        except Exception as e:
            print(e)
            dashData['pettyCash'] = 'exception'

        try:
            print(request.user.branch.purchaseOrder.latest('pk'))
            serializer = PurchaseOrderSZ(request.user.branch.purchaseOrder.latest('pk'))
            dashData['po'] = serializer.data
        except Exception as e:
            print(e)
            dashData['po'] = {
                'code': None,
                'amountTotal': None
            }

        try:
            journals = request.user.branch.journal.filter(journalDate = datetime.date.today())
            totalExpenses = Decimal(0)
            for j in journals:
                for je in j.journalentries.all():
                    if re.search('[Ee]xpense', je.accountChild.accountSubGroup.accountGroup.name):
                        if je.normally == 'Debit':
                            totalExpenses += je.amount
                        elif je.normally == 'Credit':
                            totalExpenses -= je.amount
            dashData['totalExpenses'] = totalExpenses
        except Exception as e:
            print(e)

        dashData['dueDates'] = {}
        try:
            po = request.user.branch.purchaseOrder.filter(fullyPaid = False, dueDate__gte = datetime.datetime.now(), dueDate__lte = datetime.datetime.now() + datetime.timedelta(days=14))
            serializer = PurchaseOrderSZ(po, many=True)
            if not po:
                raise Exception
            dashData['dueDates']['po'] = serializer.data
        except Exception as e:
            print(e)
            dashData['dueDates']['po'] = []

        try:
            sc = request.user.branch.salesContract.filter(fullyPaid = False, dueDate__gte = datetime.datetime.now(), dueDate__lte = datetime.datetime.now() + datetime.timedelta(days=14))
            serializer = SalesContractSZ(sc, many=True)
            if not sc:
                raise Exception
            dashData['dueDates']['sc'] = serializer.data
        except Exception as e:
            print(e)
            dashData['dueDates']['sc'] = []

        try:
            shecks = request.user.branch.cheque.filter(dueDate__gte = datetime.datetime.now())
            serializer = ChequesSZ(shecks, many = True)
            if not shecks:
                raise Exception
            dashData['dueDates']['shecks']= serializer.data
        except Exception as e:
            print(e)
            dashData['dueDates']['shecks'] = []

        dashData['monthlyExpense'] = {}
        try:
            monthlyExpense = request.user.branch.monthlyExpense.all()

            avgFunc = lambda monExp: sum([i.amount for i in monExp])/monExp.count()

            avg = avgFunc(monthlyExpense)

            monthlyExpense3 = monthlyExpense.order_by('-id')[:3]

            serializer = MonthlyExpenseSZ(monthlyExpense3, many=True)
            if not monthlyExpense:
                raise Exception
            dashData['monthlyExpense']['list'] = serializer.data
            dashData['monthlyExpense']['avg'] = avg
        except Exception as e:
            print(e)
            dashData['monthlyExpense']['list'] = None
            dashData['monthlyExpense']['avg'] = 0

        dashData['transactions'] = {}
        try:
            po = request.user.branch.purchaseOrder.all().order_by('-id')[:3]
            serializer = PurchaseOrderNestedSZ(po, many=True)
            dashData['transactions']['po'] = serializer.data
        except Exception as e:
            print(e)
            dashData['transactions']['po'] = []

        try:
            sc = request.user.branch.salesContract.all().order_by('-id')[:3]
            serializer = SalesContractSZ(sc, many=True)
            dashData['transactions']['sc'] = serializer.data
        except:
            dashData['transactions']['sc'] = []
        

        return JsonResponse(dashData, safe=False)

########## PETTY CASH ###########
class AdvancementAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AdvancementSZ
    def get_queryset(self):
        return self.request.user.branch.advancementThruPettyCash.all()

class UsersAdvancementsAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersAdvancementsSZ
    queryset = User.objects.all()
    """DOESNT NEED GET_QUERYSET"""



########## BRANCH ##########
class BranchListAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BranchSZ
    queryset = Branch.objects.all()
    """DOESNT NEED GET_QUERYSET"""





########## LIQUIDATION ##########
class LiquidationAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LiquidationSZ

    def get_queryset(self):
        return self.request.user.branch.liquidation.all()





########## RECEIVED PAYMENTS USD ##########
class ReceivedPaymentsUSDAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivedPaymentsUSDSZ
    def get_queryset(self):
        return self.request.user.branch.receivePaymentUSD.all()





########### JOB ORDER ##########
class JobOrderAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobOrderSZ
    queryset = JobOrder.objects.all()

class JobOrderAPI2(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobOrderSZ2
    queryset = JobOrder.objects.all()