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
    poitemsmerch = POItemsMerchNestedSZ(read_only=False, many=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        depth = 1





########## SALES CONTRACT ##########
class SCItemsMerchNestedSZ(serializers.ModelSerializer):
    merchInventory = MerchandiseInventoryNestedSZ(read_only=True)
    class Meta:
        model = TempSCItemsMerch
        fields= '__all__'

class SalesContractNestedSZ(serializers.ModelSerializer):
    party = PartySZ(read_only=True)
    createdBy = UserSZ(read_only=True)
    approvedBy = UserSZ(read_only=True)
    journal = JournalSZ(read_only=True)
    tempscitemsmerch = SCItemsMerchNestedSZ(read_only=True, many=True)

    class Meta:
        model = TempSalesContract
        fields = '__all__'
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

class DeliveryItemsGroup(serializers.ModelSerializer):
    deliveryitemsmerch = DeliveryItemMerchSZ(read_only=True, many=True)
    class Meta:
        model = DeliveryItemsGroup
        fields = '__all__'

class SpecialTruckSZ(serializers.ModelSerializer):
    driver = DriverSZ(read_only=True)
    deliverydestinations = DeliveryDestinationSZ(read_only=True, many=True)
    deliveryitemsgroup = DeliveryItemsGroup(read_only=True, many=True)
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
