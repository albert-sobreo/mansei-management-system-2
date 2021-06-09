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