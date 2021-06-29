from rest_framework import fields, serializers
from .models import *

########## USER ###########
class UserSZ(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'






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
    class Meta:
        model = Party
        fields = '__all__'
        depth = 1





########## WAREHOUSE ##########
class WarehouseSZ(serializers.ModelSerializer):
    class Meta: 
        model = Warehouse
        fields = '__all__'






########## MERCH INVENTORY ##########
class MerchandiseInventorySZ(serializers.ModelSerializer):
    class Meta:
        model = MerchandiseInventory
        fields = '__all__'

class MerchandiseInventoryNestedSZ(serializers.ModelSerializer):
    warehouse = WarehouseSZ(read_only=True, many=True)
    class Meta:
        model = MerchandiseInventory
        fields = '__all__'





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
        
class PurchaseOrderNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    poitemsmerch = POItemsMerchNestedSZ(read_only=True, many=True)
    poatc = POatcSZ(read_only=True, many=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        depth = 1






########## PURCHASE REQUEST ##########
class PRItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = PRItemsMerch
        fields = '__all__'

class PurchaseRequestNestedSZ(serializers.ModelSerializer):
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    pritemsmerch = PRItemsMerchNestedSZ(read_only=True, many=True)
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
        model = TempSCOtherFees(serializers.ModelSerializer)
        fields = '__all__'

class SalesContractNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    scitemsmerch = SCItemsMerchNestedSZ(read_only=True, many=True)
    scatc = SCatcSZ(read_only=True, many=True)
    scotherfees = SCOtherFeesSZ(read_only=True, many=True)

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
        depth = 1





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

class ReceivingReportNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    rritemsmerch = RRItemsMerchNestedSZ(read_only=True, many=True)
    rratc = RRatcSZ(read_only=True, many=True)

    class Meta:
        model = ReceivingReport
        fields = '__all__'
        depth = 1






# MAIN SERIALIZER
class PurchaseRequestSZ(serializers.ModelSerializer):
    pritemsmerch = PRItemsMerchSZ(read_only=True, many=True)
    vendorquotesmerch = VendorQuotesMerchSZ(read_only=True, many=True)
    class Meta:
        model = PurchaseRequest
        fields = "__all__"
        depth = 1