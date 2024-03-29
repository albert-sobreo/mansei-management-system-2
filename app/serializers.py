from rest_framework import fields, serializers
from .models import *

from rest_framework.serializers import ModelSerializer as MS

########## DEMINIMIS OF USER ##########
class DeMinimisOfUserSZ(serializers.ModelSerializer):
    class Meta:
        model = DeMinimisOfUser
        fields = "__all__"






########## USER SCHEDULE ##########
class ScheduleSZ(MS):
    class Meta:
        model = Schedule
        fields = "__all__"






########## USER LEAVE ##########
class UserLeaveSZ(MS):
    class Meta:
        model = UserLeave
        fields = "__all__"





########## USER ###########
class UserSZ(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserNameOnlySZ(serializers.ModelSerializer):
    schedule = ScheduleSZ(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'idUser',
            'id',
            'position',
            'sss',
            'image',
            'schedule'
        ]

class UserNameIDRateSZZ(serializers.ModelSerializer):
    schedule = ScheduleSZ(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'idUser',
            'rate',
            'schedule'
        ]

class RaiseSZ(MS):
    class Meta:
        model = Raise
        fields = '__all__'

class BranchSZ(MS):
    class Meta:
        model = Branch
        fields = [
            'name',
            'id'
        ]

class UserNestedSZ(serializers.ModelSerializer):
    deminimisofuser = DeMinimisOfUserSZ(read_only=True, many=True)
    userleave = UserLeaveSZ(read_only=True)
    raisse = RaiseSZ(read_only=True, many=True)
    branch = BranchSZ(read_only=True)
    schedule = ScheduleSZ(read_only=True)
    class Meta:
        model = User
        fields = [
            "address",
            "authLevel",
            "position",
            "bloodType",
            "image",
            "idUser",
            "status",
            "rate",
            "dob",
            "sss",
            "phic",
            "hdmf",
            "tin",
            "dateEmployed",
            "dateResigned",
            "department",
            "mobile",
            "schedule",
            "branch",
            "payrollable",
            "deminimisofuser",
            "id",
            "schedule",
            "userleave",
            "first_name",
            "last_name",
            "email",
            "raisse",
            'username',
            'schedule'
        ]



########## CHART OF ACCOUNTS ##########
class AccountGroupSZ(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = '__all__'

class SubGroupSZ(serializers.ModelSerializer):
    class Meta:
        model = AccountSubGroup
        fields = "__all__"

class AccountChildSZ(serializers.ModelSerializer):
    class Meta:
        model = AccountChild
        fields = '__all__'



########## CHEQUE ##########
class ChequesSZ(MS):
    class Meta:
        model = Cheques
        fields = "__all__"




class SubGroupNestedSZ(serializers.ModelSerializer):
    accountGroup = AccountGroupSZ(read_only=True)
    class Meta:
        model = AccountSubGroup
        fields = "__all__"
        depth = 1

class AccountChildNestedSZ(serializers.ModelSerializer):
    accountSubGroup = SubGroupNestedSZ(read_only=True)
    class Meta:
        model = AccountChild
        fields = "__all__"
        depth = 1
    
class AccountChildNested2SZ(serializers.ModelSerializer):
    accountSubGroup = SubGroupNestedSZ(read_only=True)
    accountchild = AccountChildSZ(read_only=True, many = True)
    class Meta:
        model = AccountChild
        fields = "__all__"
        depth = 1






########## ATC ##########
class ATCSZ(serializers.ModelSerializer):
    class Meta:
        model = ATC
        fields = '__all__'






########## PARTY ##########
class PartySZ(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class PartyNestedSZ(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class PurchaseOrderSZ(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'



class SalesContractSZ(serializers.ModelSerializer):
    class Meta:
        model = SalesContract
        fields = '__all__'

class PartyNestedTransactionSZ(serializers.ModelSerializer):
    purchaseorder = PurchaseOrderSZ(read_only = True, many = True)
    salescontract = SalesContractSZ(read_only = True, many = True)
    childAccount = AccountChildSZ(read_only=True, many=True)
    class Meta:
        model = Party
        fields = '__all__'
        depth = 1






########## MERCH INVENTORY ##########
class MerchandiseInventorySZ(serializers.ModelSerializer):
    class Meta:
        model = MerchandiseInventory
        fields = '__all__'






########## WAREHOUSE ##########
class WarehouseSZ(serializers.ModelSerializer):
    class Meta: 
        model = Warehouse
        fields = '__all__'

class WarehouseItemsSZ(serializers.ModelSerializer):
    warehouse = WarehouseSZ(read_only=True)
    class Meta:
        model=WarehouseItems
        fields='__all__'

class WarehouseItemsInventorySZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventorySZ(serializers.ModelSerializer)
    class Meta:
        model = WarehouseItems
        fields = "__all__"

class WarehouseNestedSZ(serializers.ModelSerializer):
    warehouseitems = WarehouseItemsInventorySZ(read_only=True, many=True)
    class Meta:
        model = Warehouse
        fields = "__all__"
        depth = 1






########## MERCH INVENTORY ##########


class MerchandiseInventoryNestedSZ(serializers.ModelSerializer):
    warehouseitems = WarehouseItemsSZ(read_only=True, many=True)
    childAccountInventory = AccountChildSZ(read_only=True)
    childAccountSales = AccountChildSZ(read_only=True)
    childAccountCostOfSales = AccountChildSZ(read_only=True)
    class Meta:
        model = MerchandiseInventory
        fields = '__all__'






########## OTHER INVENTORY ##########
class OtherInventorySZ(serializers.ModelSerializer):
    class Meta:
        model = OtherInventory
        fields = "__all__"




########## JOURNAL ##########
class JournalSZ(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'





########## PURCHASE ORDER ##########
class POatcSZ(serializers.ModelSerializer):
    code = ATCSZ(read_only=True)
    class Meta: 
        model = POatc
        fields = '__all__'

class POItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = POItemsMerch
        fields = '__all__'

class POItemsOtherNestedSZ(serializers.ModelSerializer):
    otherInventory = OtherInventorySZ(read_only=True)
    class Meta:
        model = POItemsOther
        fields = '__all__'
        
class PurchaseOrderNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    poitemsmerch = POItemsMerchNestedSZ(read_only=True, many=True)
    poitemsother = POItemsOtherNestedSZ(read_only=True, many=True)
    poatc = POatcSZ(read_only=True, many=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        depth = 1

class PurchaseOrderCRSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    poitemsother = POItemsOtherNestedSZ(many=True, read_only=True)
    poitemsmerch = POItemsMerchNestedSZ(many=True, read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = "__all__"





########## PURCHASE REQUEST ##########
class PRItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = PRItemsMerch
        fields = '__all__'

class PRItemsOtherSZ(serializers.ModelSerializer):
    otherInventory = OtherInventorySZ(read_only=True)
    class Meta:
        model = PRItemsOther
        fields = '__all__'

class PurchaseRequestNestedSZ(serializers.ModelSerializer):
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    pritemsmerch = PRItemsMerchNestedSZ(read_only=True, many=True)
    pritemsother = PRItemsOtherSZ(read_only=True, many=True)
    class Meta:
        model = PurchaseRequest
        fields = '__all__'
        depth = 1






        
########## INWARD INVENTORY ##########
class IIItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = IIItemsMerch
        fields = '__all__' 

class IIAdjustedItemsNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    iiItemsMerch = IIItemsMerchNestedSZ(read_only=True)
    class Meta:
        model = IIAdjustedItems
        fields = '__all__' 

class InwardInventoryNestedSZ(serializers.ModelSerializer):
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    iiitemsmerch = IIItemsMerchNestedSZ(read_only=True, many=True)
    iiadjusteditems = IIAdjustedItemsNestedSZ(read_only=True, many=True)
    class Meta:
        model = InwardInventory
        fields = '__all__'
        depth = 1






########## INWARD INVENTORY ADJUSTED ##########
class InwardInventoryAdjustedNestedSZ(serializers.ModelSerializer):
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    iiadjustedItems = IIAdjustedItemsNestedSZ(read_only=True, many=True)
    class Meta:
        model = InwardInventory
        fields = '__all__'
        depth = 1

########## SALES CONTRACT ##########
class SCItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = SCItemsMerch
        fields= '__all__'

class SCatcSZ(serializers.ModelSerializer):
    code = ATCSZ(read_only=True)
    class Meta:
        model = SCatc
        fields = '__all__'

class SCOtherFeesSZ(serializers.ModelSerializer):
    class Meta:
        model = TempSCOtherFees
        fields = '__all__'

class SalesContractNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    scotherfees = SCOtherFeesSZ(read_only=True, many=True)
    scitemsmerch = SCItemsMerchNestedSZ(read_only=True, many=True)
    scatc = SCatcSZ(read_only=True, many=True)

    class Meta:
        model = SalesContract
        fields = '__all__'
        depth = 1





########## SALES ORDER ##########
class SOItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = SOItemsMerch
        fields = '__all__'

class SOatcSZ(serializers.ModelSerializer):
    code = ATCSZ(read_only=True)
    class Meta:
        model = SOatc
        fields = '__all__'

class SOOtherFeesSZ(serializers.ModelSerializer):
    class Meta:
        model = SOOtherFees
        fields = "__all__"

class SalesOrderNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    soitemsmerch = SOItemsMerchNestedSZ(read_only=True, many=True)
    soatc = SOatcSZ(read_only=True, many=True)
    sootherfees = SOOtherFeesSZ(read_only=True, many=True)

    class Meta:
        model = SalesOrder
        fields = "__all__"
        depth = 1





########## SALES CONTRACT ##########
class SCatcSZ(serializers.ModelSerializer):
    code = ATCSZ(read_only=True)
    class Meta:
        model = SCatc
        fields = "__all__"

class SalesContractSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    scatc = SCatcSZ(read_only=True, many=True)
    class Meta:
        model = SalesContract
        fields = "__all__"
        depth = 1



    
########## SPECIAL TRUCK ##########
class DriverSZ(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class DeliveryDestinationSZ(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDestinations
        fields = "__all__"

class DeliveryItemMerchSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventorySZ(read_only=True)
    class Meta:
        model = DeliveryItemMerch
        fields = '__all__'

class DeliveryItemsGroupSZ(serializers.ModelSerializer):
    deliveryitemsmerch = DeliveryItemMerchSZ(read_only=True, many=True)
    class Meta:
        model = DeliveryItemsGroup
        fields = '__all__'

class SpecialTruckSZ(serializers.ModelSerializer):
    driver = DriverSZ(read_only=True)
    deliverydestinations = DeliveryDestinationSZ(read_only=True, many=True)
    deliveryitemsgroup = DeliveryItemsGroupSZ(read_only=True, many=True)
    class Meta:
        model = Deliveries
        fields = "__all__"
        depth = 1






########## LEDGER SPECIAL SERIALIZERS ##########
class SubGroupForLedgerSZ(serializers.ModelSerializer):
    accountGroup = AccountGroupSZ(read_only=True)
    class Meta:
        model = AccountSubGroup
        fields = '__all__'

class ChildForLedger(serializers.ModelSerializer):
    accountSubGroup = SubGroupForLedgerSZ(read_only=True)
    me = AccountChildSZ(read_only=True)
    me_too = serializers.SerializerMethodField()
    class Meta:
        model = AccountChild
        fields = [
            'id',
            'code',
            'name',
            'accountSubGroup',
            'me',
            'contra',
            'amount',
            'description',
            'me_too'
        ]

    def get_me_too(self, thisObj):
        me_too = thisObj.me_too()

        return AccountChildSZ(instance=me_too, many=True).data

class JournalEntriesForLedger(serializers.ModelSerializer):
    journal = JournalSZ(read_only=True)
    accountChild = ChildForLedger(read_only=True)
    class Meta:
        model = JournalEntries
        fields = '__all__'

class LedgerSZ(serializers.ModelSerializer):
    journalEntries = serializers.SerializerMethodField()
    accountSubGroup = SubGroupForLedgerSZ(read_only=True)
    class Meta:
        model = AccountChild
        fields = [
            'id',
            'code',
            'name',
            'accountSubGroup',
            'me',
            'contra',
            'amount',
            'description',
            'journalEntries',
        ]
    def get_journalEntries(self, thisObj):
        journalEntries = thisObj.journalentries.all()

        return JournalEntriesForLedger(instance=journalEntries, many=True).data






########## DELIVERY ##########
class DeliveryItemMerchSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventorySZ(read_only=True, many=True)
    class Meta:
        model = DeliveryItemMerch
        fields = '__all__'

class DeliveryDestinationsSZ(serializers.ModelSerializer):
    class Meta:
        model = DeliveryDestinations
        fields = '__all__'

class DeliveriesSZ(serializers.ModelSerializer):
    deliverydestinations = DeliveryDestinationsSZ(read_only=True, many=True)
    deliveryitemsgroup = DeliveryItemsGroupSZ(read_only=True, many=True)
    class Meta:
        model = Deliveries
        fields = '__all__'





########## PURCHASE REQUEST ##########
class VendorQuotesItemsMerchSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    class Meta: 
        model = VendorQuotesItemsMerch
        fields = '__all__'

class VendorQuotesMerchSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventorySZ(read_only=True)
    vendorquotesitemsmerch = VendorQuotesItemsMerchSZ(read_only=True, many=True)
    class Meta:
        model = VendorQuotesMerch
        fields = "__all__"

class PRItemsMerchSZ(serializers.ModelSerializer):
    vendorquotesmerch = VendorQuotesMerchSZ(read_only=True, many=True)
    merchInventory = MerchandiseInventorySZ(read_only=True)
    class Meta:
        model = PRItemsMerch
        fields = '__all__'





########## QUOTATIONS ##########
class QQatcSZ(serializers.ModelSerializer):
    code = ATCSZ(read_only=True)
    class Meta:
        model = QQatc
        fields = '__all__'

class QQOtherFeesSZ(serializers.ModelSerializer):
    class Meta: 
        model = QQCOtherFees
        fields = "__all__"

class QQItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = QQItemsMerch
        fields = '__all__'

class QuotationsSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    qqitemsmerch = QQItemsMerchNestedSZ(read_only=True, many=True)
    qqatc = QQatcSZ(read_only=True, many=True)
    qqotherfees = QQOtherFeesSZ(read_only=True, many=True)

    class Meta:
        model = Quotations
        fields = "__all__"
        depth = 1






########## RECEIVING REPORT ##########
class RRatcSZ(serializers.ModelSerializer):
    code = ATCSZ(read_only=True)
    class Meta: 
        model = RRatc
        fields = '__all__'

class RRItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = RRItemsMerch
        fields = '__all__'

class RRItemsOtherNestedSZ(serializers.ModelSerializer):
    otherInventory = OtherInventorySZ(read_only=True)
    class Meta:
        model = RRItemsOther
        fields = '__all__'

class ReceivingReportSZ(serializers.ModelSerializer):
    class Meta:
        model = ReceivingReport
        fields = '__all__'

class ReceivingReportCRSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    rritemsother = RRItemsOtherNestedSZ(many=True, read_only=True)
    rritemsmerch = RRItemsMerchNestedSZ(read_only=True, many=True)
    class Meta:
        model = ReceivingReport
        fields = "__all__"

class ReceivingReportNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    rritemsmerch = RRItemsMerchNestedSZ(read_only=True, many=True)
    rritemsother = RRItemsOtherNestedSZ(read_only=True, many=True)
    rratc = RRatcSZ(read_only=True, many=True)

    class Meta:
        model = ReceivingReport
        fields = '__all__'
        depth = 1

class ReceivingReportNestedSZ2(serializers.ModelSerializer):
    rritemsmerch = RRItemsMerchNestedSZ(read_only=True, many=True)
    rritemsother = RRItemsOtherNestedSZ(read_only=True, many=True)

    class Meta:
        model = ReceivingReport
        fields = "__all__"

########## VOUCHER ##########
class VoucherSZ(serializers.ModelSerializer):
    purchaseOrder = PurchaseOrderNestedSZ(read_only=True)
    class Meta:
        model = PaymentVoucher 
        fields = '__all__'
        depth = 1




########## RECEIVED PAYMENTS ##########
class ReceivedPaymentsSZ(serializers.ModelSerializer):
    salesContract = SalesContractNestedSZ(read_only=True)
    class Meta:
        model = ReceivePayment
        fields = '__all__'
        depth = 1





########## RECEIVED PAYMENT ##########
class ReceivedPayment(serializers.ModelSerializer):
    salesContract = SalesContractNestedSZ(read_only=True)
    class Meta:
        model = ReceivePayment
        fields = '__all__'
        depth = 1




########## INWARD BASIC ##########
class InwardInventorySZ(serializers.ModelSerializer):
    class Meta:
        model = InwardInventory
        fields = '__all__'
        depth = 1





########## SALES INVOICE ##########
class SalesInvoiceSZ(serializers.ModelSerializer):
    salesContract = SalesContractNestedSZ(read_only=True)
    class Meta:
        model = SalesInvoice 
        fields = '__all__'
        depth = 1

########## TRANSFER & ADJUSTMENTS ##########
class TransferItemsSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventorySZ(read_only=True)
    class Meta:
        model = TransferItems
        fields = '__all__'

class TransferPhotosSZ(serializers.ModelSerializer):
    class Meta:
        model = TransferPhotos
        fields = "__all__"

class TransferSZ(serializers.ModelSerializer):
    transferphotos = TransferPhotosSZ(many=True, read_only=True)
    tritems = TransferItemsSZ(many=True, read_only = True)
    newWarehouse = WarehouseSZ(read_only=True)
    class Meta:
        model = Transfer
        fields = '__all__'
        depth = 1

class AdjustmentItemsSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventorySZ(read_only = True)
    class Meta:
        model = AdjustmentsItems
        fields = '__all__'
        depth = 1

class AdjustmentsPhotosSZ(MS):
    class Meta:
        model = AdjustmentsPhotos
        fields = '__all__'

class AdjustmentSZ(serializers.ModelSerializer):
    aditems = AdjustmentItemsSZ(read_only = True, many=True)
    adjustmentsphotos = AdjustmentsPhotosSZ(read_only=True, many=True)
    class Meta:
        model = Adjustments
        fields = '__all__'
        depth = 1



########## BranchDefaultChildAccount ##########
class BranchDefaultChildAccountSZ(serializers.ModelSerializer):
    class Meta:
        model = BranchDefaultChildAccount
        fields = "__all__"



# MAIN SERIALIZER
class PurchaseRequestSZ(serializers.ModelSerializer):
    pritemsmerch = PRItemsMerchSZ(read_only=True, many=True)
    vendorquotesmerch = VendorQuotesMerchSZ(read_only=True, many=True)
    class Meta:
        model = PurchaseRequest
        fields = "__all__"
        depth = 1





########## DTR ##########
class DTRSZ(serializers.ModelSerializer):
    class Meta:
        model = DTR
        fields = [
            'dateTimeIn',
            'dateTimeOut',
            'date'
        ]

class UserWithDTRSZ(serializers.ModelSerializer):
    dtr = DTRSZ(read_only=True, many=True, context='what')
    schedule = ScheduleSZ(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'idUser',
            'dtr',
            'schedule'
        ]
        depth = 1

########## CR ##########
class CRSZ(serializers.ModelSerializer):
    class Meta:
        model = CompletionReport
        fields = "__all__"

class CRPOSZ(serializers.ModelSerializer):
    purchaseOrder = PurchaseOrderCRSZ(read_only=True)
    class Meta:
        model = CRPO
        fields = "__all__"

class CRSparePartsSZ(serializers.ModelSerializer):
    receivingReport = ReceivingReportCRSZ(read_only=True)
    class Meta:
        model = CRSpareParts
        fields = "__all__"




########## PPE ##########
class PPESZ(serializers.ModelSerializer):
    class Meta:
        model = PPE
        fields = '__all__'

class PPEHistoryOfDeprSZ(serializers.ModelSerializer):
    class Meta:
        model = PPEHistoryOfDepr
        fields = "__all__"


class PPENestedSZ(serializers.ModelSerializer):
    ppehistoryofdepr = PPEHistoryOfDeprSZ(read_only=True, many=True)
    completionreport = CRSZ(read_only=True, many=True)
    class Meta:
        model = PPE
        fields = "__all__"
        depth = 1

class CRNestedSZ(serializers.ModelSerializer):
    createdBy = UserNameOnlySZ(read_only=True)
    ppe = PPESZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    crpo = CRPOSZ(many=True, read_only=True)
    crspareparts = CRSparePartsSZ(many=True, read_only=True)
    class Meta:
        model = CompletionReport
        fields = "__all__"
        depth = 1



########## LEAVE AND OT REQUESTS ##########
class OTRequestSZ(serializers.ModelSerializer):
    requestedBy = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    class Meta:
        model = OTRequest
        fields = "__all__"

class UTRequestSZ(serializers.ModelSerializer):
    requestedBy = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    class Meta:
        model = UTRequest
        fields = "__all__"

class LeaveRequestSZ(serializers.ModelSerializer):
    requestedBy = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    class Meta:
        model = LeaveRequest
        fields = '__all__'





########## PAYROLL ##########
class SSSEmployeeDeductionSZ(serializers.ModelSerializer):
    class Meta:
        model = SSSEmployeeDeduction
        fields = "__all__"

class PHICEmployeeDeductionSZ(serializers.ModelSerializer):
    class Meta:
        model = PHICEmployeeDeduction
        fields = "__all__"

class PagibigEmployeeDeductionSZ(serializers.ModelSerializer):
    class Meta:
        model = PagibigEmployeeDeduction
        fields = "__all__"

class BonusPaySZ(serializers.ModelSerializer):
    class Meta:
        model = BonusPay
        fields = "__all__"

class DeMinimisPaySZ(serializers.ModelSerializer):
    class Meta:
        model = DeMinimisPay
        fields = "__all__"

class EmployeeTaxDeductionSZ(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTaxDeduction
        fields = "__all__"

class LoanDeductionSZ(serializers.ModelSerializer):
    class Meta:
        model = LoanDeduction
        fields = "__all__"

class ComplexPayrollSZ(serializers.ModelSerializer):
    user = UserNameIDRateSZZ(read_only=True)
    sssemployeededuction = SSSEmployeeDeductionSZ(read_only=True)
    phicemployeededuction = PHICEmployeeDeductionSZ(read_only=True)
    pagibigemployeededuction = PagibigEmployeeDeductionSZ(read_only=True)
    deminimispay = DeMinimisPaySZ(read_only=True, many=True)
    bonuspay = BonusPaySZ(read_only=True, many=True)
    employeetaxdeduction = EmployeeTaxDeductionSZ(read_only=True)
    loandeduction = LoanDeductionSZ(many=True, read_only=True)

    class Meta:
        model = Payroll
        fields = "__all__"
        depth = 1






########## EVERYTHING NEEDED IN PAYROLL ##########
class SSSContributionRateSZ2(serializers.ModelSerializer):
    class Meta:
        model = SSSContributionRate
        fields = "__all__"

class PHICContributionRateSZ2(serializers.ModelSerializer):
    class Meta:
        model = PHICContributionRate
        fields = "__all__"

class PagibigContributionRateSZ2(serializers.ModelSerializer):
    class Meta:
        model = PagibigContributionRate
        fields = "__all__"

class IncomeTaxTableSZ2(serializers.ModelSerializer):
    class Meta:
        model = IncomeTaxTable
        fields = "__all__"

class SSSEmployeeDeductionSZ2(MS):
    sssContributionRate = SSSContributionRateSZ2(read_only=True)
    class Meta:
        model = SSSEmployeeDeduction
        fields = [
            'ee',
            'er',
            'sssContributionRate'
        ]

class PHICEmployeeDeductionSZ2(MS):
    phicContributionRate = PHICContributionRateSZ2(read_only=True)
    class Meta:
        model = PHICEmployeeDeduction
        fields = [
            'ee',
            'er',
            'phicContributionRate'
        ]

class PagibigEmployeeDeductionSZ2(MS):
    pagibigContributionRate = PagibigContributionRateSZ2(read_only=True)
    class Meta:
        model = PagibigEmployeeDeduction
        fields = [
            'amount',
            'pagibigContributionRate'
        ]

class EmployeeTaxDeductionSZ2(MS):
    incometaxtable = IncomeTaxTableSZ2(read_only=True)
    class Meta:
        model = EmployeeTaxDeduction
        fields = [
            'amount',
            'incometaxtable',
        ]

class DeMinimisPaySZ2(MS):
    class Meta:
        model = DeMinimisPay
        fields = [
            'id',
            'name',
            'amount',
            'taxable',
        ]

class BonusPaySZ2(MS):
    class Meta:
        model = BonusPay
        fields = [
            'id',
            'name',
            'amount',
        ]

class PayrollSZ(MS):
    user = UserSZ(read_only=True)
    sssemployeededuction = SSSEmployeeDeductionSZ2(read_only=True)
    phicemployeededuction = PHICEmployeeDeductionSZ2(read_only=True)
    pagibigemployeededuction = PagibigEmployeeDeductionSZ2(read_only=True)
    employeetaxdeduction = EmployeeTaxDeductionSZ2(read_only=True)
    deminimispay = DeMinimisPaySZ2(read_only=True, many=True)
    bonuspay = BonusPaySZ2(read_only=True, many=True)

    class Meta:
        model = Payroll
        fields = "__all__"
        depth = 1

class DeMinimisSZ(MS):
    class Meta:
        model = DeMinimis
        fields = "__all__"







########## HOLIDAY ##########
class HolidaySZ(MS):
    class Meta:
        model = Holiday
        fields = "__all__"







########## PROJECT PLANNING ##########
class ProjectAssigneeSZ(MS):
    user = UserNameOnlySZ(read_only=True)
    class Meta:
        model = ProjectAssignee
        fields = "__all__"

class ProjectTaskSZ(MS):
    class Meta:
        model = ProjectTask
        fields = "__all__"

class ProjectTaskNestedSZ(MS):
    projectassignee = ProjectAssigneeSZ(many=True, read_only=True)
    class Meta:
        model = ProjectTask
        fields = "__all__"

class ProjectStageSZ(MS):
    class Meta:
        model = ProjectStage
        fields = "__all__"

class ProjectStageNestedSZ(MS):
    projecttask = ProjectTaskNestedSZ(many=True, read_only=True)
    class Meta:
        model = ProjectStage
        fields = "__all__"

class ProjectPlanSZ(MS):
    class Meta:
        model = ProjectPlan
        fields = "__all__"
        
class ProjectPlanNestedSZ(MS):
    projectstage = ProjectStageNestedSZ(many=True, read_only=True)
    projectLeader = UserNameOnlySZ(read_only=True)
    class Meta:
        model = ProjectPlan
        fields = "__all__"

class ProjectDepartmentSZ(MS):
    projectplan = ProjectPlanSZ(many=True, read_only=True)
    class Meta:
        model = ProjectDepartment
        fields = "__all__"

class ProjectDepartmentNestedSZ(MS):
    projectplan = ProjectPlanNestedSZ(many=True, read_only=True)
    class Meta:
        model = ProjectDepartment
        fields = "__all__"






########## DASHBOARD ##########
class NotepadSZ(MS):
    class Meta:
        model = Notepad
        fields = "__all__"

class UserDashboardSZ(MS):
    notepad = NotepadSZ(read_only=True)
    schedule = ScheduleSZ(read_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'id',
            'notepad',
            'authLevel',
            'schedule'
        ]

########## ANNOUNCEMENT ##########
class AnnouncementSZ(MS):
    class Meta:
        model = Announcement
        fields = "__all__"




########## BONUS 13th ###########
class Bonus13thSZ(MS):
    class Meta:
        model = Bonus13th
        fields = "__all__"

class UserWith13thSZ(MS):
    bonus13th =  Bonus13thSZ(read_only=True, many=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'id',
            'bonus13th'
        ]

########## PETTYCASH ###########
class AdvancementSZ(MS):
    issuer = UserNameOnlySZ(read_only=True)
    requestor = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    class Meta:
        model = AdvancementThruPettyCash
        fields = "__all__"

class UsersAdvancementsSZ(MS):
    advancementthrupettycashrequestor = AdvancementSZ(read_only=True, many=True)
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'advancementthrupettycashrequestor'
        ]





########## BRANCH ###########
class BranchSZ(MS):
    class Meta:
        model = Branch
        fields = [
            'id',
            'name',
        ]





########## LIQUIDATION ##########
class LiquidationEntriesSZ(MS):
    expense = AccountChildSZ(read_only=True)
    vendor = PartySZ(read_only=True)
    class Meta:
        model=LiquidationEntries
        fields = '__all__'

class LiquidationSZ(MS):
    advancement = AdvancementSZ(read_only=True)
    createdBy = UserNameOnlySZ(read_only=True)
    transactedBy = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    liquidationentries = LiquidationEntriesSZ(read_only=True, many=True)
    class Meta:
        model = Liquidation
        fields = "__all__"






########## MONTHLY EXPENSE ##########
class MonthlyExpenseSZ(MS):
    class Meta:
        model = MonthlyExpense
        fields = '__all__'






########## EXPORTS ##########
class ExportsSZ(MS):
    class Meta:
        model = Exports
        fields = "__all__"

class ExportOtherFeesSZ(MS):
    class Meta:
        model = ExportOtherFees
        fields = "__all__"

class ExportItemsMerchSZ(MS):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = ExportItemsMerch
        fields = "__all__"

class ExportNestedSZ(MS):
    exportitemsmerch = ExportItemsMerchSZ(read_only=True, many=True)
    exportotherfees = ExportOtherFeesSZ(read_only=True, many=True)
    class Meta:
        model = Exports
        fields = "__all__"
        depth = 1

class ReceivedPaymentsUSDSZ(serializers.ModelSerializer):
    exports = ExportNestedSZ(read_only=True)
    class Meta:
        model = ReceivePaymentUSD
        fields = '__all__'
        depth = 1






########## JOB ORDER ##########
class RawMaterialsNestedSZ(MS):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = RawMaterials
        fields = "__all__"

class RawMaterialsSZ(MS):
    class Meta:
        model = RawMaterials
        fields = '__all__'

class OverheadExpensesNestedSZ(MS):
    expenses = AccountChildSZ(read_only=True)
    class Meta:
        model = OverheadExpenses
        fields = "__all__"

class OverheadExpensesSZ(MS):
    class Meta:
        model = OverheadExpenses
        fields = "__all__"

class FinalProductSZ(MS):
    class Meta:
        model = FinalProduct
        fields = "__all__"

class MaterialLossesSZ(MS):
    class Meta:
        model = MaterialLosses
        fields = "__all__"

class DirectLaborSZ(MS):
    class Meta:
        model = DirectLabor
        fields = "__all__"

class JobOrderSZ(MS):
    rawmaterials = RawMaterialsNestedSZ(many=True, read_only=True)
    overheadexpenses = OverheadExpensesNestedSZ(many=True, read_only=True)
    finalproduct = FinalProductSZ(many=True, read_only=True)
    materiallosses = MaterialLossesSZ(many=True, read_only=True)
    createdBy = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    class Meta:
        model = JobOrder
        fields = "__all__"
        depth = 1

class JobOrderSZ2(MS):
    rawmaterials = RawMaterialsSZ(many=True, read_only=True)
    directlabor = DirectLaborSZ(many=True, read_only=True)
    overheadexpenses = OverheadExpensesSZ(many=True, read_only=True)
    finalproduct = FinalProductSZ(many=True, read_only=True)
    materiallosses = MaterialLossesSZ(many=True, read_only=True)
    createdBy = UserNameOnlySZ(read_only=True)
    approvedBy = UserNameOnlySZ(read_only=True)
    class Meta:
        model = JobOrder
        fields = "__all__"
        depth = 1





########## NOTIFICATIONS ###########
class NotificationsSZ(MS):
    class Meta:
        model = Notifications
        fields = "__all__"





########## MANUFACTURING INVENTORY ##########
class ManufacturingInventorySZ(MS):
    class Meta:
        model = ManufacturingInventory
        fields = "__all__"