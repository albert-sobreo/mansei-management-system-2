import decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.aggregates import Min
from django.db.models.deletion import PROTECT
from django.db.models.fields.related import OneToOneField

#CHOICES
parties = [
    ('Customer', 'Customer'),
    ('Vendor', 'Vendor')
]

normally = [
    ('Debit', 'Debit'),
    ('Credit', 'Credit'),
]

units = [
    (0, 'PC'),
    (1, 'KG'),
    (2, 'L'),
]

# Create your models here.
class Schedule(models.Model):
    timeIn = models.TimeField()
    timeOut = models.TimeField()
    workDays = models.CharField(max_length=16, null=True, blank=True)
        
    def __str__(self):
        return str(self.timeIn) + " - " + str(self.timeOut)


class User(AbstractUser):
    address = models.CharField(max_length=1024, null=True, blank=True)
    authLevel = models.CharField(max_length=50, null = True, blank = True)
    position = models.CharField(max_length=20, null = True, blank = True) 
    bloodType = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(default='profile-pictures/person.png', upload_to='profile-pictures/', null = True, blank = True)
    idUser = models.CharField(max_length=50, null = True, blank = True)
    status = models.CharField(max_length=50, null = True, blank = True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True,  default= 0.0)
    dob = models.DateField(null = True, blank = True)
    sss = models.CharField(max_length=50, null = True, blank = True)
    phic = models.CharField(max_length=50, null = True, blank = True)
    hdmf = models.CharField(max_length=50, null = True, blank = True)
    tin = models.CharField(max_length=50, null = True, blank = True)
    dateEmployed = models.DateField(null = True, blank = True)
    dateResigned = models.DateField(null = True, blank = True)
    department = models.CharField(max_length=50, null = True, blank = True)
    mobile = models.CharField(max_length=15, null = True, blank = True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey('Branch', related_name="user", on_delete=models.CASCADE, null=True, blank=True)
    payrollable = models.BooleanField(default=True)

    # DISCONNECT USER TO BRANCH IF THE USER IS NO LONGER IN THAT COMPANY

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

class Notepad(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notepad')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class UserLeave(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userleave', null=True, blank=True)
    sLeave = models.IntegerField(default=0) # sick leave
    vLeave = models.IntegerField(default=0) # vacation leave
    uLeave = models.IntegerField(default=0) # unpaid leave
    silp = models.IntegerField(default=0) # service incentive leave w pay

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class DeMinimisOfUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deminimisofuser')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

class BonusOfUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

dayOff = [
    (0, 'MON'),
    (1, 'TUE'),
    (2, 'WED'),
    (3, 'THU'),
    (4, 'FRI'),
    (5, 'SAT'),
    (6, 'SUN')
]

class Register(models.Model):
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null = True, blank = True)
    last_name = models.CharField(max_length=50, null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    password = models.CharField(max_length=255, null=True, blank=True)
    password1 = models.CharField(max_length=255, null = True, blank = True)
    password2 = models.CharField(max_length=255, null = True, blank = True)
    authLevel = models.CharField(max_length=50, null = True, blank = True)
    position = models.CharField(max_length=20, null = True, blank = True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null = True, blank = True)
    idUser = models.CharField(max_length=50, null = True, blank = True)
    status = models.CharField(max_length=50, null = True, blank = True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True,  default= 0.0)
    dob = models.DateField(null = True, blank = True)
    sss = models.CharField(max_length=50, null = True, blank = True)
    phic = models.CharField(max_length=50, null = True, blank = True)
    hdmf = models.CharField(max_length=50, null = True, blank = True)
    tin = models.CharField(max_length=50, null = True, blank = True)
    dateEmployed = models.DateField(null = True, blank = True)
    dateResigned = models.DateField(null = True, blank = True)
    department = models.CharField(max_length=50, null = True, blank = True)
    mobile = models.CharField(max_length=15, null = True, blank = True)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "Register"
        verbose_name_plural = "Registers"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.password1 = make_password(raw_password)
        self.password2 = make_password(raw_password)

    def __str__(self):
        return str(self.pk) + self.first_name + " " + self.last_name

class ATC(models.Model):
    code = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=20, decimal_places=5)
    description = models.TextField()

    def __str__(self):
        return self.code

class AccountGroup(models.Model):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    normally = models.CharField(max_length=50, choices=normally)
    permanence = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,  default= 0.0)

    class Meta:
        verbose_name = "Account Group"
        verbose_name_plural = "Account Groups"

    def __str__(self):
        return self.name + " " + self.code

class AccountSubGroup(models.Model):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    accountGroup = models.ForeignKey(AccountGroup, related_name="accountsubgroup", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,  default= 0.0)

    class Meta:
        verbose_name = "Account Sub-Group"
        verbose_name_plural = "Account Sub-Groups"

    def __str__(self):
        return self.name + " " + self.code

class AccountChild(models.Model):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    accountSubGroup = models.ForeignKey(AccountSubGroup,related_name="accountchild", on_delete=models.CASCADE, null=True, blank=True)
    me = models.ForeignKey('self', related_name="accountchild", null=True,blank=True, on_delete=models.CASCADE)
    contra = models.BooleanField(null = True, blank=True, default=False)
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,default= 0.0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Child Account"
        verbose_name_plural = "Child Accounts"

    def __str__(self):
        return self.name + " " + self.code

    def me_too(self):
        return (self.accountchild.all())

class Party(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=100, choices=parties)
    accountChild = models.ManyToManyField(AccountChild, related_name="party")
    shippingAddress = models.CharField(max_length=512, blank=True, null=True)
    officeAddress = models.CharField(max_length=512, blank=True, null=True)
    landline = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contactPerson = models.CharField(max_length=128, blank=True, null=True)
    bank = models.CharField(max_length=256, blank=True, null=True)
    bankNo = models.CharField(max_length=50, blank=True, null=True)
    tin = models.CharField(max_length=50, blank=True, null=True)
    crte = models.BooleanField(default=False)
    prefferedPayment = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"

    def __str__(self):
        return self.name + " " + self.type

class Journal(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    journalDate = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "journalCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "journalApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Journal'
        verbose_name_plural = "Journals"

    def __str__(self):
        return self.code

class JournalEntries(models.Model):
    journal = models.ForeignKey(Journal, related_name="journalentries", on_delete=models.CASCADE, null=True, blank=True)
    normally = models.CharField(max_length=50, choices=normally)
    accountChild = models.ForeignKey(AccountChild, related_name="journalentries", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,default= 0)
    balance = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,default= 0)

    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return self.normally + " " + self.accountChild.name

class Warehouse(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return self.name

class MerchandiseInventory(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=256, null = True, blank = True)
    classification = models.CharField(max_length=50, null = True, blank = True)
    type = models.CharField(max_length=50, null = True, blank = True)
    length =  models.DecimalField(max_digits=20, decimal_places=5)
    width =  models.DecimalField(max_digits=20, decimal_places=5)
    thickness =  models.DecimalField(max_digits=20, decimal_places=5)
    purchasingPrice =  models.DecimalField(max_digits=20, decimal_places=5)
    sellingPrice =  models.DecimalField(max_digits=20, decimal_places=5)
    vol = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    pricePerCubic = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    qtyT = models.IntegerField()
    qtyR = models.IntegerField()
    qtyA = models.IntegerField()
    qtyS = models.IntegerField(default = 0)
    um = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    turnover = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, default=0.00,)
    inventoryDate = models.DateField(null=True, blank=True)
    childAccountInventory = models.ForeignKey(AccountChild, on_delete=models.CASCADE, null=True, blank=True, related_name='merchinventorychildaccountinventory')
    childAccountSales = models.ForeignKey(AccountChild, on_delete=models.CASCADE, null=True, blank=True, related_name='merchinventorychildaccountsales')
    childAccountCostOfSales = models.ForeignKey(AccountChild, on_delete=models.CASCADE, null=True, blank=True, related_name='merchinventorychildaccountcostofsales')

    class Meta:
        verbose_name = "Merchandise Inventory"
        verbose_name_plural = "Merchandise Inventories"

    def __str__(self):
        return str(self.pk) + ' ' + str(self.code)

    def invAccounts(self, request, name, classification):
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        inv = "{} - {} {}".format(dChildAccount.merchInventory.name, name, classification)
        sales = '{} - {} {}'.format(dChildAccount.sales.name, name, classification)
        cos = '{} - {} {}'.format(dChildAccount.costOfSales.name, name, classification)

        if AccountChild.objects.filter(name = inv):
            objects = {
                'inv': AccountChild.objects.get(name=inv),
                'sales': AccountChild.objects.get(name=sales),
                'cos': AccountChild.objects.get(name=cos),
            }
            self.childAccountInventory = objects['inv']
            self.childAccountSales = objects['sales']
            self.childAccountCostOfSales = objects['cos']
        
        else:
            try:
                inventory = dChildAccount.merchInventory.accountSubGroup
                invCode = inventory.accountchild.latest('pk')
                invCurrentCode = int(invCode)
                invCurrentCode += 1
                invNewCode = str(invCurrentCode).zfill(4)
            except Exception as e:
                invNewCode = '0001'

            try:
                salesObj = dChildAccount.sales.accountSubGroup
                salesCode = salesObj.accountchild.latest('pk')
                salesCurrentCode = int(salesCode)
                salesCurrentCode += 1
                salesNewCode = str(salesCurrentCode).zfill(4)
            except Exception as e:
                salesNewCode = '0001'

            try:
                cosObj = dChildAccount.costOfSales.accountSubGroup
                cosCode = cosObj.accountchild.latest('pk')
                cosCurrentCode = int(cosCode)
                cosCurrentCode += 1
                cosNewCode = str(cosCurrentCode).zfill(4)
            except Exception as e:
                cosNewCode = '0001'

            childInventory = AccountChild.objects.create(code = invNewCode, name = inv, accountSubGroup = dChildAccount.merchInventory.accountSubGroup, me = dChildAccount.merchInventory, amount = 0.0, description = "")
            childSales = AccountChild.objects.create(code=salesNewCode, name=sales, accountSubGroup=dChildAccount.sales.accountSubGroup, me=dChildAccount.sales, amount=0, description='')
            childCoS = AccountChild.objects.create(code=cosNewCode, name=cos, accountSubGroup=dChildAccount.costOfSales.accountSubGroup, me=dChildAccount.costOfSales, amount=0, description='')

            childInventory.save()
            childSales.save()
            childCoS.save()

            self.childAccountInventory = childInventory
            self.childAccountSales = childSales
            self.childAccountCostOfSales = childCoS
            
            request.user.branch.accountChild.add(childInventory)
            request.user.branch.accountChild.add(childSales)
            request.user.branch.accountChild.add(childCoS)
        self.save()

class OtherInventory(models.Model):
    name = models.CharField(max_length=100)
    qty = models.IntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5, default=0.00)
    accountChild = models.ForeignKey(AccountChild, on_delete=models.CASCADE, blank=True, null=True)
        

    class Meta:
        verbose_name = "Other Inventory"
        verbose_name_plural = "Other Inventories"

    def __str__(self):
        return self.name
    
class WarehouseItems(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name = 'warehouseitems')
    merchInventory = models.ForeignKey(MerchandiseInventory, on_delete=models.CASCADE, related_name = 'warehouseitems')
    qtyT = models.IntegerField()
    qtyR = models.IntegerField()
    qtyA = models.IntegerField()
    qtyS = models.IntegerField(default = 0)

    def __str__(self):
        return self.merchInventory.code

    def initQty(self, qtyT, qtyR, qtyA):
        self.qtyT = qtyT
        self.qtyR = qtyR
        self.qtyA = qtyA
        self.qtyS = 0
        return 1

    def save2(self):
        self.merchInventory.save()
        self.save()
    
    def addQty(self, qty):
        self.qtyA += qty
        self.qtyT += qty
        self.merchInventory.qtyA += qty
        self.merchInventory.qtyT += qty

        if self.qtyA < 0 or self.qtyT < 0 or self.merchInventory.qtyA < 0 or self.merchInventory.qtyT < 0:
            return 0

        return 1

    def resQty(self, qty):
        self.qtyR += qty
        self.qtyA -= qty

        self.merchInventory.qtyR += qty
        self.merchInventory.qtyA -= qty

        if self.qtyR < 0 or self.qtyA < 0 or self.merchInventory.qtyR < 0 or self.merchInventory.qtyA < 0:
            return 0

        return 1

    def salesWSO(self, qty):
        self.qtyR -= qty
        self.qtyS += qty

        self.merchInventory.qtyR -= qty
        self.merchInventory.qtyS += qty

        if self.qtyR < 0 or self.qtyS < 0 or self.merchInventory.qtyR < 0 or self.merchInventory.qtyS < 0:
            return 0

        return 1

    def salesWOSO(self, qty):
        self.qtyA -= qty
        self.qtyS += qty

        self.merchInventory.qtyA -= qty
        self.merchInventory.qtyS += qty

        if self.qtyA < 0 or self.qtyS < 0 or self.merchInventory.qtyA < 0 or self.merchInventory.qtyS < 0:
            return 0

        return 1

class Cheques(models.Model):
    chequeNo = models.CharField(max_length=255, null=True, blank=True)
    accountChild = models.ForeignKey(AccountChild, on_delete=models.CASCADE, null = True, blank = True, related_name="cheques")
    approved = models.BooleanField(null = True, default=False, blank = True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="cheApprovedBy")
    datetimeApproved = models.DateTimeField(null = True, blank = True)
    dueDate = models.DateField(null = True, blank = False)

class PurchaseRequest(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateRequested = models.DateField()
    dateNeeded = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    intendedFor = models.CharField(max_length=200, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "prCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "prApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    poed = models.BooleanField(default = False)
    voided = models.BooleanField(null = True, default = False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name = "prVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)
    

    class Meta:
        verbose_name = "Purchase Request"
        verbose_name_plural = "Purchase Requests"

    def __str__(self):
        return self.code


class PRItemsMerch(models.Model):    
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="pritemsmerch",on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="pritemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    unit = models.IntegerField(choices=units, null=True, blank=True)

    class Meta:
        verbose_name = 'PR Items Merch'
        verbose_name_plural = "PR Items Merchs"

    def __str__(self):
        return self.purchaseRequest.code + " - " + self.merchInventory.code

class PRItemsOther(models.Model):
    type = models.CharField(max_length = 255, blank=True, null=True)
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="pritemsother",on_delete=models.CASCADE, null=True, blank=True)
    otherInventory = models.ForeignKey(OtherInventory, related_name="pritemsother", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    unit = models.IntegerField(choices=units, null=True, blank=True)

    class Meta:
        verbose_name = "PR Items Other"
        verbose_name_plural = "PR Items Others"

    def __str__(self):
        return self.purchaseRequest.code + " - " + self.otherInventory.name

class PurchaseOrder(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    datePurchased = models.DateField()
    party = models.ForeignKey(Party, related_name="purchaseorder", on_delete=models.CASCADE)
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="purchaseorder",on_delete=models.CASCADE, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    amountDue = models.DecimalField(max_digits=20, decimal_places=5)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5)
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    paymentMethod = models.CharField(max_length=50, null=True, blank=True)
    paymentPeriod = models.CharField(max_length=50)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "poCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "poApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default=False)
    journal = models.ForeignKey(Journal, related_name="purchaseorder", on_delete=models.CASCADE, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, blank = True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    fullyReceived = models.BooleanField(default=False)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True, default = 0.0)
    voided = models.BooleanField(null = True, default= False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "poVoidedBy")
    datetimeVoided = models.DateTimeField(null=True, blank=True)
    needsRR = models.BooleanField(default = True)

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
        return self.code

class POItemsMerch(models.Model):
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="poitemsmerch",on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="poitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=5)
    delivered = models.BooleanField(null = True, default=False)
    qtyReceived = models.IntegerField(default=0)
    unit = models.IntegerField(choices=units, null=True, blank=True)

    class Meta:
        verbose_name = 'PO Items Merch'
        verbose_name_plural = "PO Items Merchs"

    def __str__(self):
        return self.purchaseOrder.code + " - " + self.merchInventory.code

class POItemsOther(models.Model):
    type = models.CharField(max_length = 255, blank=True, null=True)
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="poitemsother",on_delete=models.CASCADE, null=True, blank=True)
    otherInventory = models.ForeignKey(OtherInventory, related_name="poitemsother", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=5)
    delivered = models.BooleanField(null = True, default=False)
    qtyReceived = models.IntegerField(default=0)
    unit = models.IntegerField(choices=units, null=True, blank=True)

class POatc(models.Model):
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="poatc",on_delete=models.CASCADE, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="poatc",on_delete=models.CASCADE, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    
class ReceivingReport(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateReceived = models.DateField()
    party = models.ForeignKey(Party, related_name="receivingreport", on_delete=models.CASCADE)
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="receivingreport",on_delete=models.CASCADE, null=True, blank=True)
    amountDue = models.DecimalField(max_digits=20, decimal_places=5)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5)
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "rrCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "rrApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default=False)
    journal = models.ForeignKey(Journal, related_name="receivingreport", on_delete=models.CASCADE, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, blank=True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    qtyReceived = models.IntegerField(null = True, blank = True)
    fullyReceived = models.BooleanField(null = True, blank = True)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    voided = models.BooleanField(null = True, default = False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name = "rrVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)
    first = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = "Receiving Report"
        verbose_name_plural = "Receiving Reports"

    def __str__(self):
        return self.code

class RRItemsMerch(models.Model):
    receivingReport = models.ForeignKey(ReceivingReport, related_name="rritemsmerch",on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="rritemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=5)
    delivered = models.BooleanField(null = True, default=False)
    poitemsmerch = models.ForeignKey(POItemsMerch, related_name='rritemsmerch', on_delete=models.CASCADE, null=True, blank=True)
    unit = models.IntegerField(choices=units, null=True, blank=True)

    class Meta:
        verbose_name = 'RR Items Merch'
        verbose_name_plural = "RR Items Merchs"

    def __str__(self):
        return self.receivingReport.code + " - " + self.merchInventory.code

class RRItemsOther(models.Model):
    type = models.CharField(max_length = 255, blank=True, null=True)
    receivingReport = models.ForeignKey(ReceivingReport, related_name="rritemsother",on_delete=models.CASCADE, null=True, blank=True)
    otherInventory = models.ForeignKey(OtherInventory, related_name="rritemsother", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=5)
    delivered = models.BooleanField(null = True, default=False)
    poitemsother = models.ForeignKey(POItemsOther, related_name='rritemsother', on_delete=models.CASCADE, null=True, blank=True)
    unit = models.IntegerField(choices=units, null=True, blank=True)

class RRatc(models.Model):
    receivingReport = models.ForeignKey(ReceivingReport, related_name="rratc",on_delete=models.CASCADE, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="rratc",on_delete=models.CASCADE, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)

class InwardInventory(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateInward = models.DateField()
    party = models.ForeignKey(Party, related_name="inwardinventory", on_delete=models.CASCADE, null=True, blank=True)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "iiCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "iiApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default = False)
    adjustedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "iiAdjustedBy")
    datetimeAdjusted = models.DateTimeField(null=True, blank=True)
    adjusted = models.BooleanField(null = True, default = False)
    journal = models.ForeignKey(Journal, related_name="inwardinventory", on_delete=models.CASCADE, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, blank=True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    voided = models.BooleanField(null = True, default = False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name = "iiVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)
    first = models.BooleanField(null = True, default = False)

class IIItemsMerch(models.Model):
    inwardInventory = models.ForeignKey(InwardInventory, related_name="iiitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="iiitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField()
    pricePerCubic = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    code = models.CharField(max_length=50, null = True, blank = True)
    name = models.CharField(max_length=50, null = True, blank = True)
    classfication = models.CharField(max_length=50, null = True, blank = True)
    type = models.CharField(max_length=50, null = True, blank = True)
    length = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True)
    width = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True)
    thicc = models.DecimalField(max_digits=20, decimal_places=2, null = True, blank = True)
    vol = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)

class IIAdjustedItems(models.Model):
    inwardInventory = models.ForeignKey(InwardInventory, related_name="iiadjusteditems", on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="iiadjusteditems", on_delete=models.CASCADE, null=True, blank=True)
    iiItemsMerch = models.ForeignKey(IIItemsMerch, related_name="iiadjusteditems", on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField()
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null = True, blank = True)
    classfication = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=20, decimal_places=2, null = True)
    width = models.DecimalField(max_digits=20, decimal_places=2, null = True)
    thicc = models.DecimalField(max_digits=20, decimal_places=2, null = True)
    vol = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=20, decimal_places=5, null = True)

class Quotations(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateQuoted = models.DateField()
    party = models.ForeignKey(Party, related_name="quotations", on_delete=models.CASCADE, null=True, blank=True)
    amountDue = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5)
    discountPercent = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "qCreatedBy")
    remarks = models.TextField(null = True, blank=True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "qApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    qqd = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"

    def __str__(self):
        return self.code


class QQItemsMerch(models.Model):
    quotations = models.ForeignKey(Quotations, related_name="qqitemsmerch",on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="qqitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, related_name="qqitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    cbm = models.CharField(max_length=10, null = True)
    vol = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        verbose_name = 'QQ Items Merch'
        verbose_name_plural = "QQ Items Merchs"

    def __str__(self):
        return self.quotations.code + " - " + self.merchInventory.code

class QQCOtherFees(models.Model):
    quotations = models.ForeignKey(Quotations, related_name="qqotherfees",on_delete=models.CASCADE, null=True, blank=True)
    fee = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, null = True)

class QQatc(models.Model):
    quotations = models.ForeignKey(Quotations, related_name="qqatc",on_delete=models.CASCADE, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="qqatc",on_delete=models.CASCADE, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)

class SalesOrder(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateSold = models.DateField()
    party = models.ForeignKey(Party, related_name="salesorder", on_delete=models.CASCADE, null=True, blank=True)
    quotations = models.ForeignKey(Quotations, related_name = "salesorder", on_delete = models.CASCADE, null = True, blank = True)
    amountDue = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5)
    discountPercent = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, null = True, blank = True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "soCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "soApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default = False)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    voided = models.BooleanField(null = True, default = False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name = "soVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)
    soed = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orders"

    def __str__(self):
        return self.code

    
class SOItemsMerch(models.Model):
    salesOrder = models.ForeignKey(SalesOrder, related_name="soitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="soitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.IntegerField()
    cbm = models.CharField(max_length=10, null = True)
    vol = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    delivered = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = 'SO Items Merch'
        verbose_name_plural = "SO Items Merchs"

    def __str__(self):
        return self.salesOrder.code + " - " + self.merchInventory.code

class SOOtherFees(models.Model):
    salesOrder = models.ForeignKey(SalesOrder, related_name="sootherfees", on_delete=models.CASCADE, null=True, blank=True)
    fee = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, null = True)

class SOatc(models.Model):
    salesOrder = models.ForeignKey(SalesOrder, related_name="soatc", on_delete=models.CASCADE, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="soatc",on_delete=models.CASCADE, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)


class SalesContract(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateSold = models.DateField()
    party = models.ForeignKey(Party, related_name="salescontract", on_delete=models.CASCADE, null=True, blank=True)
    salesOrder = models.ForeignKey(SalesOrder, related_name="salescontract", on_delete=models.CASCADE, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null = True)
    amountDue = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5)
    discountPercent = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    paymentMethod = models.CharField(max_length=50, null=True, blank=True)
    paymentPeriod = models.CharField(max_length=50, null=True, blank=True)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, null = True, blank = True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "tempscCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "tempscApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default = False)
    voided = models.BooleanField(null = True, default = False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name= "scVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)
    journal = models.ForeignKey(Journal, related_name="salescontract", on_delete=models.CASCADE, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, blank=True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    

    class Meta:
        verbose_name = "Sales Contract"
        verbose_name_plural = "Sales Contract"

    def __str__(self):
        return self.code

class PaymentVoucher(models.Model):
    code = models.CharField(max_length = 50, null = True, blank=True)
    datetimeCreated = models.DateTimeField(null = True, blank=True)
    paymentDate = models.DateField(null = True, blank=True)
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name= "paymentvoucher", on_delete=models.CASCADE, null = True, blank=True)
    transaction = models.ForeignKey(SalesContract, related_name= "paymentvoucher", on_delete=models.CASCADE, null = True, blank=True )
    receivingReport = models.ForeignKey(ReceivingReport, related_name= "paymentvoucher", on_delete=models.CASCADE, null = True, blank=True)
    inwardInventory = models.ForeignKey(InwardInventory, related_name= "paymentvoucher", on_delete=models.CASCADE, null = True, blank = True)
    journal = models.ForeignKey(Journal, related_name= "paymentvoucher", on_delete=models.CASCADE, null = True, blank=True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="vCreatedBy")
    approved = models.BooleanField(default = 'False', null = True, blank = True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="vApprovedBy")
    datetimeApproved = models.DateTimeField(null = True, blank=True)
    paymentMethod = models.CharField(max_length = 50, null = True, blank=True)
    paymentPeriod = models.CharField(max_length = 50, null = True, blank = True)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True, default = 0.0)
    amountPaid = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    voided = models.BooleanField(null = True, default = False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name = "pvVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)
    first = models.BooleanField(null = True, default = False, blank=True)
    cheque = models.ForeignKey(Cheques, related_name= "paymentvoucher", on_delete=models.CASCADE, null = True, blank = True )
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True)

class CustomPVEntries(models.Model):
    paymentVoucher = models.ForeignKey(PaymentVoucher, related_name="custompventries", on_delete=models.CASCADE, null=True, blank=True)
    normally = models.CharField(max_length=50, choices=normally)
    accountChild = models.ForeignKey(AccountChild, related_name="custompventries", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,default= 0)

class TempSalesContract(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateSold = models.DateField()
    party = models.ForeignKey(Party, related_name="tempsalescontract", on_delete=models.CASCADE, null=True, blank=True)
    subTotal = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    discountPercent = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "scCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "scApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    journal = models.ForeignKey(Journal, related_name="tempsalescontract", on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    

class TempSCItemsMerch(models.Model):
    salesContract = models.ForeignKey(TempSalesContract, related_name='tempscitemsmerch', on_delete=models.CASCADE)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="tempscitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.IntegerField()
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    delivered = models.BooleanField(null = True, default=False)

class TempSCOtherFees(models.Model):
    salesContract = models.ForeignKey(SalesContract, related_name='scotherfees', on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=20, decimal_places=5)
    description = models.CharField(max_length=255, null = True)

class SCItemsMerch(models.Model):
    salesContract = models.ForeignKey(SalesContract, related_name="scitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="scitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.IntegerField()
    cbm = models.CharField(max_length=10, null = True)
    vol = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    delivered = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = "SC Items Merch"
        verbose_name_plural = "SC Items Merchs"

    def __str__(self):
        return self.merchInventory.code

class SCatc(models.Model):
    salesContract = models.ForeignKey(SalesContract, related_name="scatc",on_delete=models.CASCADE, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="scatc",on_delete=models.CASCADE, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)


class SalesInvoice(models.Model):
    code = models.CharField(max_length = 50, null = True)
    datetimeCreated = models.DateTimeField(null = True)
    paymentDate = models.DateField(null = True)
    salesOrder = models.ForeignKey(SalesOrder, related_name= "salesinvoice", on_delete=models.CASCADE, null = True)
    salesContract = models.ForeignKey(SalesContract, related_name= "salesinvoice", on_delete=models.CASCADE, null = True)
    journal = models.ForeignKey(Journal, related_name= "salesinvoice", on_delete=models.CASCADE, null = True)
    remarks = models.TextField(null = True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="siCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="siApprovedBy")
    datetimeApproved = models.DateTimeField(null = True)
    paymentMethod = models.CharField(max_length = 50, null = True)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    amountPaid = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)

class VendorQuotesMerch(models.Model):
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="vendorquotesmerch",on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="vendorquotesmerch", on_delete=models.CASCADE, null=True, blank=True)

class VendorQuotesItemsMerch(models.Model):
    vendorquotesmerch = models.ForeignKey(VendorQuotesMerch, related_name="vendorquotesitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=5)
    party = models.ForeignKey(Party, related_name="vendorquotesitemsmerch", on_delete=models.CASCADE)

class ReceivePayment(models.Model):
    code = models.CharField(max_length=50, null = True)
    datetimeCreated = models.DateTimeField(null = True)
    paymentDate = models.DateField(null = True)
    salesContract = models.ForeignKey(SalesContract, related_name= "receivepayment", on_delete=models.CASCADE, null = True)
    transaction = models.ForeignKey(PurchaseOrder, related_name= "receivepayment", on_delete=models.CASCADE, null = True )
    journal = models.ForeignKey(Journal, related_name= "receivepayment", on_delete=models.CASCADE, null = True)
    remarks = models.TextField(null = True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="rpCreatedBy")
    paymentMethod = models.CharField(max_length = 50, null = True)
    paymentPeriod = models.CharField(max_length = 50, null = True)
    amountPaid = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    wep = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True, default= 0.0)
    voided = models.BooleanField(default = False)
    cheque = models.ForeignKey(Cheques, related_name= "receivepayment", on_delete=models.CASCADE, null = True, blank = True )
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True)

class CustomRPEntries(models.Model):
    receivePayment = models.ForeignKey(ReceivePayment, related_name="customrpentries", on_delete=models.CASCADE, null=True, blank=True)
    normally = models.CharField(max_length=50, choices=normally)
    accountChild = models.ForeignKey(AccountChild, related_name="customrpentries", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True,default= 0)

class Driver(models.Model):
    driverID = models.CharField(max_length=50, default='0')
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Available')
    
    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return self.firstName + " " + self.lastName

class Truck(models.Model):
    plate = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null = True, default = 'Available')
    currentDelivery = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Truck"
        verbose_name_plural = "Trucks"

    def __str__(self):
        return self.brand + "-" + self.model + " " + self.plate

class Deliveries(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated =  models.DateTimeField()
    truck = models.ForeignKey(Truck, related_name="deliveries", on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, related_name="deliveries", on_delete=models.CASCADE, null=True, blank=True)
    scheduleStart = models.DateTimeField(null=True, blank=True)
    scheduleEnd = models.DateTimeField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="deCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True , related_name="deApprovedBy")
    approved = models.BooleanField(null = True, default=False)
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    amountTotal = models.DecimalField(max_digits=20, decimal_places=5)
    voided = models.BooleanField(null = True, default=False)
    voidedBy = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name="deVoidedBy")
    datetimeVoided = models.DateTimeField(null = True, blank = True)

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

    def __str__(self):
        return self.code

class DeliveryDestinations(models.Model):
    deliveries = models.ForeignKey(Deliveries, related_name='deliverydestinations', on_delete=models.CASCADE, null=True, blank=True)
    destination = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Delivery Destination"
        verbose_name_plural = "Delivery Destinations"

    def __str__(self):
        return self.deliveries.code

class DeliveryPhotos(models.Model):
    deliveries = models.ForeignKey(Deliveries, related_name="deliveryphotos", on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to="delivery_photos")

    class Meta:
        verbose_name = "Delivery Photo"
        verbose_name_plural = "Delivery Photos"

    def __str__(self):
        return self.deliveries.code

class DeliveryItemsGroup(models.Model):
    deliveries = models.ForeignKey(Deliveries, related_name="deliveryitemsgroup", on_delete=models.CASCADE, null=True, blank=True)
    deliveryType = models.CharField(max_length=50)
    referenceNo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Delivery Item Group"
        verbose_name_plural = "Delivery Item Groups"

    def __str__(self):
        return self.deliveries.code

class DeliveryItemMerch(models.Model):
    deliveryItemsGroup = models.ForeignKey(DeliveryItemsGroup, related_name="deliveryitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="deliveryitemsmerch", on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField()

    class Meta:
        verbose_name = "Delivery Item Merch"
        verbose_name_plural = "Delivery Item Merchs"

    def __str__(self):
        return self.merchInventory.code + ' ' + self.merchInventory.classification + ' ' + self.merchInventory.type

class Transfer(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "trCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "trApprovedBy")
    approved = models.BooleanField(null = True, default=False)
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    newWarehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null = True, blank = True, related_name= "transfer")
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)

class TransferItems(models.Model):
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="tritems", on_delete=models.CASCADE, null=True, blank=True)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, null = True, blank = True, related_name= "tritems")
    qtyTransfered = models.IntegerField(null = True, blank = True)
    oldWarehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null = True, blank = True, related_name= "tritems")


class Adjustments(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "adCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "adApprovedBy")
    approved = models.BooleanField(null = True, default=False)
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    totalLost = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    type = models.CharField(max_length=50)

class AdjustmentsItems(models.Model):
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="aditems", on_delete=models.CASCADE, null=True, blank=True)
    adjustments = models.ForeignKey(Adjustments, on_delete=models.CASCADE, null = True, blank = True, related_name= "aditems")
    qtyAdjusted = models.IntegerField(null = True, blank = True)
    remaining = models.IntegerField(null = True, blank = True)
    unitCost = models.DecimalField(max_digits = 20, decimal_places=5, null = True, blank = True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    oldWarehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null = True, blank = True, related_name= "aditems")

class AdjustmentsPhotos(models.Model):
    adjustments = models.ForeignKey(Deliveries, related_name="adjustmentsphotos", on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to="adjustment_photos")

class PPE(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=512, null=True, blank=True)
    type = models.CharField(max_length=128, null=True, blank=True)
    purchaseDate = models.DateField(null=True, blank=True)
    accumDepr = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    bookValue = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    usefulLife = models.IntegerField(null=True, blank=True)
    purchasePrice = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    deprCycle = models.IntegerField(null=True, blank=True) # BASIS: MONTH
    startingDeprDate = models.DateField(null=True, blank=True)
    deprRate = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return str(self.code) + " " + self.name + " " + self.type

class PPEHistoryOfDepr(models.Model):
    ppe = models.ForeignKey(PPE, on_delete=models.CASCADE, related_name="ppehistoryofdepr", null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    deprAmount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    accumDeprAmount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    bookValue = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)    

class TestUploadFile(models.Model):
    file = models.ImageField(upload_to='test/')

class CompletionReport(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='completionreportcreatedby')
    reportDate = models.DateField(null=True, blank=True)
    ppe = models.ForeignKey(PPE, on_delete=models.CASCADE, null=True, blank=True, related_name='completionreport')
    malfuncDate = models.DateField(null=True, blank=True)
    damageDescription = models.TextField(null=True, blank=True)
    spareParts = models.ForeignKey(ReceivingReport, on_delete=models.CASCADE, null=True, blank=True, related_name='completionreport')
    damagePhoto = models.ImageField(null=True, blank=True, upload_to="cr/damage/")
    recommendation = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    successPhoto = models.ImageField(null=True, blank=True, upload_to="cr/success/")
    approved = models.BooleanField(default=False)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='completionreportapprovedby')
    datetimeApproved = models.DateTimeField(null = True, blank=True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    capitalized = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class CRSpareParts(models.Model):
    cr = models.ForeignKey(CompletionReport, on_delete=models.CASCADE, related_name='crspareparts')
    receivingReport = models.ForeignKey(ReceivingReport, on_delete=models.CASCADE, related_name='crspareparts')

    def __str__(self):
        return self.cr.code + " --- " + self.receivingReport.code

class CRPO(models.Model):
    cr = models.ForeignKey(CompletionReport, on_delete=models.CASCADE, related_name='crpo')
    purchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='crpo')

    def __str__(self):
        return self.cr.code + " --- " + self.purchaseOrder.code

class Holiday(models.Model):
    date = models.DateField()
    year = models.CharField(max_length=6)
    description = models.CharField(max_length=512)
    type = models.CharField(max_length=100)

    def __str__(self):
        return str(self.date) + " " + self.description

class Payroll(models.Model):
    year = models.CharField(max_length=6, blank=True, null=True)
    dateStart = models.DateField(null=True, blank=True)
    dateEnd = models.DateField(null=True, blank=True)
    dateGenerated = models.DateField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='payrollapprovedby')
    dateApproved = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payroll")
    previousPayroll = models.OneToOneField('self', related_name='previouspayroll', null=True, blank=True, on_delete=models.SET_NULL)

    bh = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    ot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    ut = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    nd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    ndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdnd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rh = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhnd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    sh = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shnd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shw = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwnd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdnd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdnd = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdndot = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)

    bhTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    otTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    utTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    ndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    ndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rdndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shwndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    rhrdndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdndTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    shrdndotTotalHours = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)

    basicPay = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    holidayPay = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    grossPayBeforeBonus = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    grossPayAfterBonus = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    netPayBeforeTaxes = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    netPayAfterTaxes = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Loans(models.Model):
    user = models.ForeignKey(User, related_name='loans', on_delete=models.PROTECT, null=True, blank=True)
    year = models.CharField(max_length=6, null=True, blank=True)
    dateCreated = models.DateField(null=True, blank=True)
    startOfAmortization = models.DateField(null=True, blank=True)
    endOfAmortization = models.DateField(null=True, blank=True)
    loanType = models.CharField(max_length=256, null=True, blank=True)
    loanFrom = models.CharField(max_length=128, null=True, blank=True)
    loanAmount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    serviceFee = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    serviceFeeRate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    netProceeds = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    interestAmount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    interestRate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    totalWithInterest = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    monthlyAmortization = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True, default=0)
    fullyPaid = models.BooleanField(default=False)

class DeMinimisPay(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="deminimispay")
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deminimispay')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    taxable = models.BooleanField(default=False)

class BonusPay(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bonuspay")
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name="bonuspay", null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

class Bonus13th(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bonus13th")
    year = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

class DayOff(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    day = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.day)

class DTR(models.Model):
    dateTimeIn = models.DateTimeField( null = True, blank = True)
    dateTimeOut = models.DateTimeField( null = True, blank = True)
    date = models.DateField( null = True, blank = True)
    user = models.ForeignKey(User, related_name = "dtr", on_delete=models.PROTECT, null = True, blank = True)
    payroll = models.ForeignKey(Payroll, related_name='dtr', on_delete=models.SET_NULL, null=True, blank=True)

    bh = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ut = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    nd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rdot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rdnd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rdndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rh = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhnd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    sh = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shnd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shw = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shwot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shwnd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shwndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhrd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhrdot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhrdnd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    rhrdndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shrd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shrdot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shrdnd = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    shrdndot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    
    normalDay = models.BooleanField(default=True)

class DTRDayCategory(models.Model):
    dtr = models.ForeignKey(DTR, on_delete=models.CASCADE, related_name="dtrdaycategory")
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE, related_name="dtrdaycategory")

class RatesGroup(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    bh = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    ot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    ut = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    nd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    ndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rdot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rdnd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rdndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rh = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhnd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    sh = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shnd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shw = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shwot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shwnd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shwndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhrd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhrdot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhrdnd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    rhrdndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shrd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shrdot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shrdnd = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    shrdndot = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    def __str__(self):
        return self.name

class OTRequest(models.Model):
    requestedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otrequestrequestedby') 
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='otrequestapprovedby')
    status = models.CharField(max_length=64, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    datetimeCreated = models.DateTimeField(null=True, blank=True)
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    dtr = models.ForeignKey(DTR, related_name='otrequest', on_delete=models.SET_NULL, null=True, blank=True, default=None)

class UTRequest(models.Model):
    requestedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utrequestrequestedby")
    timeOut = models.TimeField()
    date = models.DateField()
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='utrequestapprovedby')
    status = models.CharField(max_length=64, null=True, blank=True)
    datetimeCreated = models.DateTimeField(null=True, blank=True)
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    dtr = models.ForeignKey(DTR, on_delete=models.SET_NULL, null=True, blank=True, default=None)

class LeaveRequest(models.Model):
    requestedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaverequestrequestedby')
    dateStart = models.DateField()
    dateEnd = models.DateField()
    reason = models.TextField(null=True, blank=True)
    leaveType = models.CharField(max_length=64, null=True, blank=True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="leaverequestapprovedby")
    datetimeCreated = models.DateTimeField(null=True, blank=True)
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=64, null=True, blank=True)

class SSSContributionRate(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    upperLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lowerLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    er = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name + "   " + str(self.lowerLimit) + " --- " + str(self.upperLimit)

class PHICContributionRate(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    upperLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lowerLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name + "   " + str(self.lowerLimit) + " --- " + str(self.upperLimit)

class PagibigContributionRate(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name + "   " + str(self.rate)

class SSSEmployeeDeduction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payroll = models.OneToOneField(Payroll, related_name="sssemployeededuction", on_delete=models.CASCADE, null=True, blank=True)
    ee = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    er = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sssContributionRate = models.ForeignKey(SSSContributionRate, related_name="sssemployeededuction", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "   " + str(self.payroll.dateStart) + " --- " + str(self.payroll.dateEnd)

class PHICEmployeeDeduction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payroll = models.OneToOneField(Payroll, related_name="phicemployeededuction", on_delete=models.CASCADE, null=True, blank=True)
    ee = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    er = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    phicContributionRate = models.ForeignKey(PHICContributionRate, related_name="phicemployeededuction", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "   " + str(self.payroll.dateStart) + " --- " + str(self.payroll.dateEnd)

class PagibigEmployeeDeduction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payroll = models.OneToOneField(Payroll, related_name="pagibigemployeededuction", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    pagibigContributionRate = models.ForeignKey(PagibigContributionRate, related_name="pagibigemployeededuction", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "   " + str(self.payroll.dateStart) + " --- " + str(self.payroll.dateEnd)

class IncomeTaxTable(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    lowerLimit = models.DecimalField(max_digits=16, decimal_places=0, null=True, blank=True)
    upperLimit = models.DecimalField(max_digits=16, decimal_places=0, null=True, blank=True)
    fixedDeduction = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    percentDeduction = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class EmployeeTaxDeduction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payroll = models.OneToOneField(Payroll, related_name="employeetaxdeduction", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    incometaxtable = models.ForeignKey(IncomeTaxTable, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "   " + str(self.payroll.dateStart) + " --- " + str(self.payroll.dateEnd)

class LoanDeduction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payroll = models.ForeignKey(Payroll, related_name="loandeduction", on_delete=models.CASCADE, null=True, blank=True)
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE, related_name="loandeduction", null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    loanFrom = models.CharField(max_length=128, null=True, blank=True)

class DeMinimis(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    limit = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.name

class TaxableDeMinimisPay(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="taxabledeminimispay")
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='taxabledeminimispay')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " --- " + self.name

class Payslip(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='payslip')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="payslip")

class Raise(models.Model):
    user = models.ForeignKey(User, related_name='raisse', on_delete=models.SET_NULL, null=True, blank=True)
    previousRate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    newRate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

class Position(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class MonthlyExpense(models.Model):
    year = models.CharField(max_length=6)
    date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=5, default=0)

    def __str__(self):
        return str(self.date)

class ProjectDepartment(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class ProjectPlan(models.Model):
    name = models.CharField(max_length=255)
    dateStart = models.DateField(null=True, blank=True)
    dateEnd = models.DateField(null=True, blank=True)
    dateCreated = models.DateField(null=True, blank=True)
    dateCompleted = models.DateField(null=True, blank=True)
    projectLeader = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projectplan')
    department = models.ForeignKey(ProjectDepartment, on_delete=models.CASCADE, null=True, blank=True, related_name="projectplan")
    accentColor = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.name

class ProjectStage(models.Model):
    name = models.CharField(max_length=255)
    accentColor = models.CharField(max_length=12, null=True, blank=True)
    projectPlan = models.ForeignKey(ProjectPlan, on_delete=models.CASCADE, null=True, blank=True, related_name="projectstage")

    def __str__(self):
        return self.name

class ProjectTask(models.Model):
    name = models.CharField(max_length=255)
    datetimeStart = models.DateTimeField(null=True, blank=True)
    datetimeEnd = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    projectStage = models.ForeignKey(ProjectStage, null=True, blank=True, on_delete=models.CASCADE, related_name="projecttask")

    def __str__(self):
        return self.name

class ProjectAssignee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="projectassignee")
    projectTask = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, null=True, blank=True, related_name="projectassignee")

    def __str__(self):
        return self.projectTask.name + " --- " + self.user.first_name + " " + self.user.last_name

class Annualization(models.Model):
    excel = models.FileField(upload_to='files/')
    name = models.CharField(max_length=50, null = True, blank = True)
    year = models.CharField(max_length=50, null = True, blank = True)

class AdvancementThruPettyCash(models.Model):
    code = models.CharField(max_length=50)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="advancementthrupettycashrequestor")
    issuer  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="advancementthrupettycashissuer")
    amount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True) 
    datetimeCreated = models.DateTimeField()
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approvedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name= "advancementthrupettycashApprovedBy")
    approved = models.BooleanField(null = True, default=False)
    reason = models.TextField(null = True, blank=True)

class BranchDefaultChildAccount(models.Model):
    ##### CASH AND CASH EQUIVALENTS #####
    rm = models.ForeignKey(AccountChild, related_name="branchdefaultrm", on_delete=models.CASCADE, null=True, blank=True)
    defaultWarehouse = models.ForeignKey(Warehouse, related_name = 'branchdefaultwarehouse', on_delete=models.CASCADE, blank = True, null = True)
    cashOnHand = models.ForeignKey(AccountChild, related_name='branchcashonhand', on_delete=models.CASCADE, blank=True, null=True)
    cashInBank = models.ManyToManyField(AccountChild, related_name='branchcashinbank', blank=True)
    pettyCash = models.ForeignKey(AccountChild, related_name='branchpettycash', on_delete=models.CASCADE, blank=True, null=True)
    merchInventory = models.ForeignKey(AccountChild, related_name='branchmerchinventory', on_delete=models.CASCADE, blank=True, null=True)
    manuInventory = models.ForeignKey(AccountChild, related_name='branchmanuinventory', on_delete=models.CASCADE, blank=True, null=True)
    ppeProperty = models.ForeignKey(AccountChild, related_name='branchppeproperty', on_delete=models.CASCADE, blank=True, null=True)
    ppePlant = models.ForeignKey(AccountChild, related_name='branchppeplant', on_delete=models.CASCADE, blank=True, null=True)
    ppeEquipment = models.ForeignKey(AccountChild, related_name='branchppeequipment', on_delete=models.CASCADE, blank=True, null=True)
    inputVat = models.ForeignKey(AccountChild, related_name='branchinputvat', on_delete=models.CASCADE, blank=True, null=True)
    outputVat = models.ForeignKey(AccountChild, related_name="branchoutputvat", on_delete=models.CASCADE, blank=True, null=True)
    ewp = models.ForeignKey(AccountChild, related_name='branchewp', on_delete=models.CASCADE, blank=True, null=True)
    advancesToSupplier = models.ManyToManyField(AccountChild, related_name="branchadvancestosupplier", blank=True)
    prepaidExpense = models.ForeignKey(AccountChild, related_name="branchprepaidexpense", on_delete=models.CASCADE, blank = True, null = True)
    sales = models.ForeignKey(AccountChild, related_name="branchsales", on_delete=models.CASCADE, blank = True, null = True)
    costOfSales = models.ForeignKey(AccountChild, related_name="branchcostofsales", on_delete=models.CASCADE, blank = True, null = True)
    otherIncome = models.ForeignKey(AccountChild, related_name="branchotherincome", on_delete=models.CASCADE, blank = True, null = True)
    revenue = models.ForeignKey(AccountChild, related_name="branchrevenue", on_delete=models.CASCADE, blank = True, null = True)
    cwit = models.ForeignKey(AccountChild, related_name="branchcwit", on_delete=models.CASCADE, blank = True, null = True)
    salariesExpense = models.ForeignKey(AccountChild, related_name="branchsalariesexpense", on_delete=models.CASCADE, blank = True, null = True)
    bonus = models.ForeignKey(AccountChild, related_name="branchbonus", on_delete=models.CASCADE, blank = True, null = True)    
    monthPay13 = models.ForeignKey(AccountChild, related_name="branchmonthpay13", on_delete=models.CASCADE, blank = True, null = True)
    deminimisBenefit = models.ForeignKey(AccountChild, related_name="branchdeminimisbenefit", on_delete=models.CASCADE, blank = True, null = True)
    hdmfShare = models.ForeignKey(AccountChild, related_name="branchhdmfshare", on_delete=models.CASCADE, blank = True, null = True)
    phicERShare = models.ForeignKey(AccountChild, related_name="branchphicershare", on_delete=models.CASCADE, blank = True, null = True)
    sssERShare = models.ForeignKey(AccountChild, related_name="branchsssershare", on_delete=models.CASCADE, blank = True, null = True)
    salariesPayable = models.ForeignKey(AccountChild, related_name="branchsalariespayable", on_delete=models.CASCADE, blank = True, null = True)
    sssPayable = models.ForeignKey(AccountChild, related_name="branchssspayable", on_delete=models.CASCADE, blank = True, null = True)
    phicPayable = models.ForeignKey(AccountChild, related_name="branchphicpayable", on_delete=models.CASCADE, blank = True, null = True)
    hdmfPayable = models.ForeignKey(AccountChild, related_name="branchhdmfpayable", on_delete=models.CASCADE, blank = True, null = True)
    withholdingTaxPayable = models.ForeignKey(AccountChild, related_name="branchwithholdingtaxpayable", on_delete=models.CASCADE, blank = True, null = True)

class BranchProfile(models.Model):
    branchDefaultChildAccount = models.ForeignKey(BranchDefaultChildAccount, related_name='branchprofile', on_delete=models.CASCADE, null=True, blank=True)

# request.user.branch.accountChild.add()
class Branch(models.Model):
    name = models.CharField(max_length=255)
    ##### DEFAULT PETTY CASH REPLENISH #####
    pettyCashReplenish =  models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True) 
    branchProfile = models.ForeignKey(BranchProfile, related_name='branch', on_delete=models.CASCADE, null=True, blank=True)
    ##### CHART OF ACCOUNTS #####
    accountGroup = models.ManyToManyField(AccountGroup, blank = True)
    subGroup = models.ManyToManyField(AccountSubGroup, blank = True)
    accountChild = models.ManyToManyField(AccountChild, blank = True)

    ##### VENDORS AND CUSTOMER #####
    party = models.ManyToManyField(Party, blank = True)

    ##### ACCOUNTING #####
    journal = models.ManyToManyField(Journal, blank = True)
    journalEntries = models.ManyToManyField(JournalEntries, blank = True)

    ##### INVENTORY #####
    warehouse = models.ManyToManyField(Warehouse, blank = True)
    warehouseItems = models.ManyToManyField(WarehouseItems, blank=True)
    merchInventory = models.ManyToManyField(MerchandiseInventory, blank = True)

    otherInventory = models.ManyToManyField(OtherInventory, blank=True)

    ##### PURCHASE REQUEST #####
    purchaseRequest = models.ManyToManyField(PurchaseRequest, blank = True)
    pritemsMerch = models.ManyToManyField(PRItemsMerch, blank = True)
    prItemsOther = models.ManyToManyField(PRItemsOther, blank=True)

    ##### VENDOR QUOTES #####
    vendorQuotesMerch = models.ManyToManyField(VendorQuotesMerch, blank = True)
    vendorQuotesItemsMerch = models.ManyToManyField(VendorQuotesItemsMerch, blank=True)

    ##### PURCHASE ORDER #####
    purchaseOrder = models.ManyToManyField(PurchaseOrder, blank = True)
    poitemsMerch = models.ManyToManyField(POItemsMerch, blank = True)
    poItemsOther = models.ManyToManyField(POItemsOther, blank = True)
    poatc = models.ManyToManyField(POatc, blank=True)

    ##### RECEIVING REPORT #####
    receivingReport = models.ManyToManyField(ReceivingReport, blank = True)
    rritemsMerch = models.ManyToManyField(RRItemsMerch, blank = True)
    rrItemsOther = models.ManyToManyField(RRItemsOther, blank=True)
    rratc = models.ManyToManyField(RRatc, blank = True)

    ##### QUOTATIONS #####
    quotations = models.ManyToManyField(Quotations, blank = True)
    qqitemsMerch = models.ManyToManyField(QQItemsMerch, blank = True)
    qqOtherFees = models.ManyToManyField(QQCOtherFees, blank = True)
    qqatc = models.ManyToManyField(QQatc, blank = True)

    ##### SALES ORDER #####
    salesOrder = models.ManyToManyField(SalesOrder, blank = True)
    soitemsMerch = models.ManyToManyField(SOItemsMerch, blank = True)
    soOtherFees = models.ManyToManyField(SOOtherFees, blank = True)
    soatc = models.ManyToManyField(SOatc, blank = True)

    ##### SALES CONTRACT #####
    salesContract = models.ManyToManyField(SalesContract, blank = True)
    scitemsMerch = models.ManyToManyField(SCItemsMerch, blank = True)
    tempSCOtherFees = models.ManyToManyField(TempSCOtherFees, blank = True)
    scatc = models.ManyToManyField(SCatc, blank = True)

    ##### DELIVERIES #####
    driver = models.ManyToManyField(Driver, blank = True)
    truck = models.ManyToManyField(Truck, blank = True)
    deliveries = models.ManyToManyField(Deliveries, blank = True)
    deliveriesDestination = models.ManyToManyField(DeliveryDestinations, blank = True)
    deliveryPhotos = models.ManyToManyField(DeliveryPhotos, blank = True)
    deliveryitemsGroup = models.ManyToManyField(DeliveryItemsGroup, blank = True)
    deliveryitemsMerch = models.ManyToManyField(DeliveryItemMerch, blank = True)

    ##### INWARD #####
    inwardInventory = models.ManyToManyField(InwardInventory, blank=True)
    iiItemsMerch = models.ManyToManyField(IIItemsMerch, blank=True)
    iiAdjustedItems = models.ManyToManyField(IIAdjustedItems, blank=True)

    #### PAYMENT VOUCHER & SALES INVOICE ####
    paymentVoucher = models.ManyToManyField(PaymentVoucher, blank = True)
    customPVEntries = models.ManyToManyField(CustomPVEntries, blank=True)
    salesInvoice = models.ManyToManyField(SalesInvoice, blank = True)
    receivePayment = models.ManyToManyField(ReceivePayment, blank = True)
    customRPEntries = models.ManyToManyField(CustomRPEntries, blank=True)

    #### TRANSFER AND ADJUSTMENTS ####
    transfer = models.ManyToManyField(Transfer, blank = True)
    transferItems = models.ManyToManyField(TransferItems, blank = True)
    adjustments = models.ManyToManyField(Adjustments, blank = True)
    adjustmentItems = models.ManyToManyField(AdjustmentsItems, blank = True)
    adjustmentPhotos = models.ManyToManyField(AdjustmentsPhotos, blank = True)

    #### DTR ####
    dayOff = models.ManyToManyField(DayOff, blank=True)
    dtr = models.ManyToManyField(DTR, blank=True)
    schedule = models.ManyToManyField(Schedule, blank=True)

    #### CHEQUE ####
    cheque = models.ManyToManyField(Cheques, blank=True)

    #### PPE ####
    ppe = models.ManyToManyField(PPE, blank=True)
    ppeHistoryOfDepr = models.ManyToManyField(PPEHistoryOfDepr, blank=True)

    #### COMPLETION REPORT ####
    completionReport = models.ManyToManyField(CompletionReport, blank=True)
    crSpareParts = models.ManyToManyField(CRSpareParts, blank=True)
    crpo = models.ManyToManyField(CRPO, blank=True)

    #### DTR 2 ####
    holiday = models.ManyToManyField(Holiday, blank=True)
    dtrDayCategory = models.ManyToManyField(DTRDayCategory, blank=True)
    otRequest = models.ManyToManyField(OTRequest, blank=True)
    utRequest = models.ManyToManyField(UTRequest, blank=True)
    leaveRequest = models.ManyToManyField(LeaveRequest, blank=True)
    ratesGroup = models.ManyToManyField(RatesGroup, blank=True)

    #### PAYROLL ####
    payroll = models.ManyToManyField(Payroll, blank=True)
    deMinimisOfUser = models.ManyToManyField(DeMinimisOfUser, blank=True)
    deMinimisPay = models.ManyToManyField(DeMinimisPay, blank=True)

    bonusOfUser = models.ManyToManyField(BonusOfUser, blank=True)
    bonusPay = models.ManyToManyField(BonusPay, blank=True)

    #### EMPLOYEE DEDUCTIONS ####
    sssEmployeeDeduction = models.ManyToManyField(SSSEmployeeDeduction, blank=True)
    phicEmployeeDeduction = models.ManyToManyField(PHICEmployeeDeduction, blank=True)
    pagibigEmployeeDeduction = models.ManyToManyField(PagibigEmployeeDeduction, blank=True)

    #### PAYSLIP ####
    payslip = models.ManyToManyField(Payslip, blank=True)

    #### RAISE ####
    race = models.ManyToManyField(Raise, blank=True) # changed spelling because raise is a reserved word

    #### BRANCH POSITIONS ####
    position = models.ManyToManyField(Position, blank=True)

    #### LOANS ####
    loans = models.ManyToManyField(Loans, blank=True)
    loanDeduction = models.ManyToManyField(LoanDeduction, blank=True)

    #### MONTHLY EXPENSE ####
    monthlyExpense = models.ManyToManyField(MonthlyExpense, blank=True)

    #### PROJECT PLANNER ####
    projectDepartment = models.ManyToManyField(ProjectDepartment, blank=True)
    projectPlan = models.ManyToManyField(ProjectPlan, blank=True)
    projectStage = models.ManyToManyField(ProjectStage, blank=True)
    projectTask = models.ManyToManyField(ProjectTask, blank=True)
    projectAssignee = models.ManyToManyField(ProjectAssignee, blank=True)

    #### 13TH MONTH PAY ####
    bonus13th = models.ManyToManyField(Bonus13th, blank=True)

    #### ANNUALIZATION ####
    annualization = models.ManyToManyField(Annualization, blank = True)

    #### PETTY CASH ####
    advancementThruPettyCash = models.ManyToManyField(AdvancementThruPettyCash, blank = True)
    

    def __str__(self):
        return self.name

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    contents = models.TextField(null = True, blank=True)
    branch = models.ForeignKey(Branch, related_name="branchannouncement", on_delete=models.CASCADE)

