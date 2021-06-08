from rest_framework import fields, serializers
from .models import *

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