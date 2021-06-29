from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.aggregates import Min
from django.db.models.deletion import PROTECT

#CHOICES
parties = [
    ('Customer', 'Customer'),
    ('Vendor', 'Vendor')
]

normally = [
    ('Debit', 'Debit'),
    ('Credit', 'Credit'),
]

# Create your models here.
class User(AbstractUser):
    authLevel = models.CharField(max_length=50, null = True, blank = True)
    position = models.CharField(max_length=20, null = True, blank = True)
    image = models.ImageField(default='profile-pictures/person.png', upload_to='profile-pictures/', null = True, blank = True)
    idUser = models.CharField(max_length=50, null = True, blank = True)
    status = models.CharField(max_length=50, null = True, blank = True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True,  default= 0.0)
    dob = models.DateField(null = True, blank = True)
    sss = models.CharField(max_length=50, null = True, blank = True)
    phic = models.CharField(max_length=50, null = True, blank = True)
    hdmf = models.CharField(max_length=50, null = True, blank = True)
    tin = models.CharField(max_length=50, null = True, blank = True)
    dateEmployed = models.DateField(null = True, blank = True)
    dateResigned = models.DateField(null = True, blank = True)
    department = models.CharField(max_length=50, null = True, blank = True)
    mobile = models.CharField(max_length=15, null = True, blank = True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

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
    rate = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True,  default= 0.0)
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
    rate = models.DecimalField(max_digits=10, decimal_places=5)
    description = models.TextField()

    def __str__(self):
        return self.code

class AccountGroup(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    normally = models.CharField(max_length=50, choices=normally)
    permanence = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True,  default= 0.0)

    class Meta:
        verbose_name = "Account Group"
        verbose_name_plural = "Account Groups"

    def __str__(self):
        return self.name + " " + self.code

class AccountSubGroup(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    accountGroup = models.ForeignKey(AccountGroup, related_name="accountsubgroup", on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True,  default= 0.0)

    class Meta:
        verbose_name = "Account Sub-Group"
        verbose_name_plural = "Account Sub-Groups"

    def __str__(self):
        return self.name + " " + self.code

class AccountChild(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    accountSubGroup = models.ForeignKey(AccountSubGroup,related_name="accountchild", on_delete=models.PROTECT, null=True, blank=True)
    me = models.ForeignKey('self', related_name="accountchild", null=True,blank=True, on_delete=models.PROTECT)
    contra = models.BooleanField(null = True, blank=True, default=False)
    amount = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True,default= 0.0)
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
    crte = models.BooleanField(blank=True, null = True)
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
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name= "journalCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "journalApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Journal'
        verbose_name_plural = "Journals"

    def __str__(self):
        return self.code

class JournalEntries(models.Model):
    journal = models.ForeignKey(Journal, related_name="journalentries", on_delete=models.PROTECT, null=True, blank=True)
    normally = models.CharField(max_length=50, choices=normally)
    accountChild = models.ForeignKey(AccountChild, related_name="journalentries", on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True,default= 0)
    balance = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True,default= 0)

    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return self.journal.code + " " + self.normally + " " + self.accountChild.name

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
    name = models.CharField(max_length=50, null = True, blank = True)
    classification = models.CharField(max_length=50, null = True, blank = True)
    type = models.CharField(max_length=50, null = True, blank = True)
    length =  models.DecimalField(max_digits=20, decimal_places=5)
    width =  models.DecimalField(max_digits=20, decimal_places=5)
    thickness =  models.DecimalField(max_digits=20, decimal_places=5)
    purchasingPrice =  models.DecimalField(max_digits=18, decimal_places=5)
    sellingPrice =  models.DecimalField(max_digits=18, decimal_places=5)
    vol = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    pricePerCubic = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    qtyT = models.IntegerField()
    qtyR = models.IntegerField()
    qtyA = models.IntegerField()
    um = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=5, null = True, blank=True)
    warehouse = models.ManyToManyField(Warehouse, related_name="merchandiseinventory", blank=True)
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, default=0.00,)

    class Meta:
        verbose_name = "Merchandise Inventory"
        verbose_name_plural = "Merchandise Inventories"

    def __str__(self):
        return str(self.pk) + ' ' + str(self.code)
    

class PurchaseRequest(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateRequested = models.DateField()
    dateNeeded = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    intendedFor = models.CharField(max_length=200, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "prCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "prApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    poed = models.BooleanField(default = False)
    

    class Meta:
        verbose_name = "Purchase Request"
        verbose_name_plural = "Purchase Requests"

    def __str__(self):
        return self.code


class PRItemsMerch(models.Model):
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="pritemsmerch",on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="pritemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'PR Items Merch'
        verbose_name_plural = "PR Items Merchs"

    def __str__(self):
        return self.purchaseRequest.code + " - " + self.merchInventory.code

class PurchaseOrder(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    datePurchased = models.DateField()
    party = models.ForeignKey(Party, related_name="purchaseorder", on_delete=models.PROTECT)
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="purchaseorder",on_delete=models.PROTECT, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=18, decimal_places=5)
    amountDue = models.DecimalField(max_digits=18, decimal_places=5)
    amountTotal = models.DecimalField(max_digits=18, decimal_places=5)
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    paymentMethod = models.CharField(max_length=50)
    paymentPeriod = models.CharField(max_length=50)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "poCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "poApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default=False)
    journal = models.ForeignKey(Journal, related_name="purchaseorder", on_delete=models.PROTECT, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, blank = True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    fullyReceived = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
        return self.code

class POItemsMerch(models.Model):
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="poitemsmerch",on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="poitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=5)
    delivered = models.BooleanField(null = True, default=False)
    qtyReceived = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'PO Items Merch'
        verbose_name_plural = "PO Items Merchs"

    def __str__(self):
        return self.purchaseOrder.code + " - " + self.merchInventory.code

class POatc(models.Model):
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="poatc",on_delete=models.PROTECT, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="poatc",on_delete=models.PROTECT, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)
    
class ReceivingReport(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateReceived = models.DateField()
    party = models.ForeignKey(Party, related_name="receivingreport", on_delete=models.PROTECT)
    purchaseOrder = models.ForeignKey(PurchaseOrder, related_name="receivingreport",on_delete=models.PROTECT, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=18, decimal_places=5)
    amountDue = models.DecimalField(max_digits=18, decimal_places=5)
    amountTotal = models.DecimalField(max_digits=18, decimal_places=5)
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True)
    paymentMethod = models.CharField(max_length=50)
    paymentPeriod = models.CharField(max_length=50)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "rrCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "rrApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default=False)
    journal = models.ForeignKey(Journal, related_name="receivingreport", on_delete=models.PROTECT, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    qtyReceived = models.IntegerField(null = True, blank = True)
    fullyReceived = models.BooleanField(null = True, blank = True)

    class Meta:
        verbose_name = "Receiving Report"
        verbose_name_plural = "Receiving Reports"

    def __str__(self):
        return self.code

class RRItemsMerch(models.Model):
    receivingReport = models.ForeignKey(ReceivingReport, related_name="rritemsmerch",on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="rritemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    purchasingPrice = models.DecimalField(max_digits=20, decimal_places=5)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=5)
    delivered = models.BooleanField(null = True, default=False)
    poitemsmerch = models.ForeignKey(POItemsMerch, related_name='rritemsmerch', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'RR Items Merch'
        verbose_name_plural = "RR Items Merchs"

    def __str__(self):
        return self.receivingReport.code + " - " + self.merchInventory.code

class RRatc(models.Model):
    receivingReport = models.ForeignKey(ReceivingReport, related_name="rratc",on_delete=models.PROTECT, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="rratc",on_delete=models.PROTECT, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)

class InwardInventory(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateInward = models.DateField()
    party = models.ForeignKey(Party, related_name="inwardinventory", on_delete=models.PROTECT, null=True, blank=True)
    amountTotal = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "iiCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "iiApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default = False)
    adjustedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "iiAdjustedBy")
    datetimeAdjusted = models.DateTimeField(null=True, blank=True)
    adjusted = models.BooleanField(null = True, default = False)
    journal = models.ForeignKey(Journal, related_name="inwardinventory", on_delete=models.PROTECT, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)

class IIItemsMerch(models.Model):
    inwardInventory = models.ForeignKey(InwardInventory, related_name="iiitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="iiitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    qty = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    code = models.CharField(max_length=50)
    productMark = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    thicc = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    vol = models.DecimalField(max_digits=10, decimal_places=5, null = True)

class IIAdjustedItems(models.Model):
    inwardInventory = models.ForeignKey(InwardInventory, related_name="iiadjusteditems", on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="iiadjusteditems", on_delete=models.PROTECT, null=True, blank=True)
    iiItemsMerch = models.ForeignKey(IIItemsMerch, related_name="iiadjusteditems", on_delete=models.PROTECT, null=True, blank=True)
    qty = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50, null = True, blank = True)
    classfication = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    thicc = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    vol = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=10, decimal_places=5, null = True)

class Quotations(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateQuoted = models.DateField()
    party = models.ForeignKey(Party, related_name="quotations", on_delete=models.PROTECT, null=True, blank=True)
    amountDue = models.DecimalField(max_digits=18, decimal_places=5, null = True)
    amountTotal = models.DecimalField(max_digits=18, decimal_places=5)
    discountPercent = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "qCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "qApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"

    def __str__(self):
        return self.code


class QQItemsMerch(models.Model):
    quotations = models.ForeignKey(Quotations, related_name="qqitemsmerch",on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="qqitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.PositiveIntegerField()
    cbm = models.CharField(max_length=10, null = True)
    vol = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=18, decimal_places=5)

    class Meta:
        verbose_name = 'QQ Items Merch'
        verbose_name_plural = "QQ Items Merchs"

    def __str__(self):
        return self.quotations.code + " - " + self.merchInventory.code

class QQCOtherFees(models.Model):
    quotations = models.ForeignKey(Quotations, related_name="qqotherfees",on_delete=models.PROTECT, null=True, blank=True)
    fee = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, null = True)

class QQatc(models.Model):
    quotations = models.ForeignKey(Quotations, related_name="qqatc",on_delete=models.PROTECT, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="qqatc",on_delete=models.PROTECT, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)

class SalesOrder(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateSold = models.DateField()
    party = models.ForeignKey(Party, related_name="salesorder", on_delete=models.PROTECT, null=True, blank=True)
    quotations = models.ForeignKey(Quotations, related_name = "salesorder", on_delete = models.PROTECT, null = True, blank = True)
    amountPaid = models.DecimalField(max_digits=18, decimal_places=5, null = True)
    amountDue = models.DecimalField(max_digits=18, decimal_places=5, null = True)
    amountTotal = models.DecimalField(max_digits=18, decimal_places=5)
    discountPercent = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    paymentMethod = models.CharField(max_length=50)
    paymentPeriod = models.CharField(max_length=50)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, null = True, blank = True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "soCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "soApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orders"

    def __str__(self):
        return self.code

    
class SOItemsMerch(models.Model):
    salesOrder = models.ForeignKey(SalesOrder, related_name="soitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="soitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.IntegerField()
    cbm = models.CharField(max_length=10, null = True)
    vol = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    delivered = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = 'SO Items Merch'
        verbose_name_plural = "SO Items Merchs"

    def __str__(self):
        return self.salesOrder.code + " - " + self.merchInventory.code

class SOOtherFees(models.Model):
    salesOrder = models.ForeignKey(SalesOrder, related_name="sootherfees", on_delete=models.PROTECT, null=True, blank=True)
    fee = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, null = True)

class SOatc(models.Model):
    salesOrder = models.ForeignKey(SalesOrder, related_name="soatc", on_delete=models.PROTECT, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="soatc",on_delete=models.PROTECT, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)


class SalesContract(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateSold = models.DateField()
    party = models.ForeignKey(Party, related_name="salescontract", on_delete=models.PROTECT, null=True, blank=True)
    salesOrder = models.ForeignKey(SalesOrder, related_name="salescontract", on_delete=models.PROTECT, null=True, blank=True)
    amountPaid = models.DecimalField(max_digits=18, decimal_places=5, null = True)
    amountDue = models.DecimalField(max_digits=18, decimal_places=5, null = True)
    amountTotal = models.DecimalField(max_digits=18, decimal_places=5)
    discountPercent = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxType = models.CharField(max_length=20, null = True, blank = True)
    taxRate = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank=True)
    paymentMethod = models.CharField(max_length=50)
    paymentPeriod = models.CharField(max_length=50)
    chequeNo = models.CharField(max_length=50, null=True, blank=True)
    dueDate = models.DateField(null = True, blank = True)
    bank = models.CharField(max_length=50, null = True, blank = True)
    remarks = models.TextField(null = True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "tempscCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "tempscApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default = False)
    journal = models.ForeignKey(Journal, related_name="salescontract", on_delete=models.PROTECT, null=True, blank=True)
    fullyPaid = models.BooleanField(null = True, default = False)
    runningBalance = models.DecimalField(max_digits=20, decimal_places=5, null = True, blank = True)
    

    class Meta:
        verbose_name = "Sales Contract"
        verbose_name_plural = "Sales Contract"

    def __str__(self):
        return self.code

class TempSalesContract(models.Model):
    code = models.CharField(max_length=50)
    datetimeCreated = models.DateTimeField()
    dateSold = models.DateField()
    party = models.ForeignKey(Party, related_name="tempsalescontract", on_delete=models.PROTECT, null=True, blank=True)
    subTotal = models.DecimalField(max_digits=15, decimal_places=5, validators=[MinValueValidator(0)])
    discountPercent = models.DecimalField(max_digits=10, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    discountPeso = models.DecimalField(max_digits=20, decimal_places=5,null=True, blank=True, validators=[MinValueValidator(0)])
    taxPeso = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "scCreatedBy")
    approvedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name= "scApprovedBy")
    datetimeApproved = models.DateTimeField(null=True, blank=True)
    journal = models.ForeignKey(Journal, related_name="tempsalescontract", on_delete=models.PROTECT, null=True, blank=True)
    approved = models.BooleanField(default=False)
    

class TempSCItemsMerch(models.Model):
    salesContract = models.ForeignKey(TempSalesContract, related_name='tempscitemsmerch', on_delete=models.PROTECT)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="tempscitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.IntegerField()
    totalCost = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    delivered = models.BooleanField(null = True, default=False)

class TempSCOtherFees(models.Model):
    salesContract = models.ForeignKey(SalesContract, related_name='scotherfees', on_delete=models.PROTECT)
    fee = models.DecimalField(max_digits=20, decimal_places=5, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, null = True)

class SCItemsMerch(models.Model):
    salesContract = models.ForeignKey(SalesContract, related_name="scitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="scitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    remaining = models.IntegerField()
    qty = models.IntegerField()
    cbm = models.CharField(max_length=10, null = True)
    vol = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    pricePerCubic = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    totalCost = models.DecimalField(max_digits=10, decimal_places=5, null = True)
    delivered = models.BooleanField(null = True, default = False)

    class Meta:
        verbose_name = "SC Items Merch"
        verbose_name_plural = "SC Items Merchs"

    def __str__(self):
        return self.merchInventory.name

class SCatc(models.Model):
    salesContract = models.ForeignKey(SalesContract, related_name="scatc",on_delete=models.PROTECT, null=True, blank=True)
    code = models.ForeignKey(ATC, related_name="scatc",on_delete=models.PROTECT, null=True, blank=True)
    amountWithheld = models.DecimalField(max_digits=18, decimal_places=5, blank=True, null=True)

class VendorQuotesMerch(models.Model):
    purchaseRequest = models.ForeignKey(PurchaseRequest, related_name="vendorquotesmerch",on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="vendorquotesmerch", on_delete=models.PROTECT, null=True, blank=True)

class VendorQuotesItemsMerch(models.Model):
    vendorquotesmerch = models.ForeignKey(VendorQuotesMerch, related_name="vendorquotesitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(max_digits=18, decimal_places=5)
    party = models.ForeignKey(Party, related_name="vendorquotesitemsmerch", on_delete=models.PROTECT)

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
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, null=True, blank=True)
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
    truck = models.ForeignKey(Truck, related_name="deliveries", on_delete=models.PROTECT, null=True, blank=True)
    driver = models.ForeignKey(Driver, related_name="deliveries", on_delete=models.PROTECT, null=True, blank=True)
    scheduleStart = models.DateTimeField(null=True, blank=True)
    scheduleEnd = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(null = True, default=False)
    datetimeApproved = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

    def __str__(self):
        return self.code

class DeliveryDestinations(models.Model):
    deliveries = models.ForeignKey(Deliveries, related_name='deliverydestinations', on_delete=models.PROTECT, null=True, blank=True)
    destination = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Delivery Destination"
        verbose_name_plural = "Delivery Destinations"

    def __str__(self):
        return self.destination + ' ' + self.deliveries.code

class DeliveryPhotos(models.Model):
    deliveries = models.ForeignKey(Deliveries, related_name="deliveryphotos", on_delete=models.PROTECT, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to="delivery_photos")

    class Meta:
        verbose_name = "Delivery Photo"
        verbose_name_plural = "Delivery Photos"

    def __str__(self):
        return self.deliveries.code

class DeliveryItemsGroup(models.Model):
    deliveries = models.ForeignKey(Deliveries, related_name="deliveryitemsgroup", on_delete=models.PROTECT, null=True, blank=True)
    deliveryType = models.CharField(max_length=50)
    referenceNo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Delivery Item Group"
        verbose_name_plural = "Delivery Item Groups"

    def __str__(self):
        return self.deliveries.code

class DeliveryItemMerch(models.Model):
    deliveryItemsGroup = models.ForeignKey(DeliveryItemsGroup, related_name="deliveryitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    merchInventory = models.ForeignKey(MerchandiseInventory, related_name="deliveryitemsmerch", on_delete=models.PROTECT, null=True, blank=True)
    qty = models.IntegerField()

    class Meta:
        verbose_name = "Delivery Item Merch"
        verbose_name_plural = "Delivery Item Merchs"

    def __str__(self):
        return self.merchInventory.code + ' ' + self.merchInventory.classification + ' ' + self.merchInventory.type


class Branch(models.Model):
    name = models.CharField(max_length=255)
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
    merchInventory = models.ManyToManyField(MerchandiseInventory, blank = True)

    ##### PURCHASE REQUEST #####
    purchaseRequest = models.ManyToManyField(PurchaseRequest, blank = True)
    pritemsMerch = models.ManyToManyField(PRItemsMerch, blank = True)

    ##### VENDOR QUOTES #####
    vendorQuotesMerch = models.ManyToManyField(VendorQuotesMerch, blank = True)
    vendorQuotesItemsMerch = models.ManyToManyField(VendorQuotesItemsMerch, blank=True)

    ##### PURCHASE ORDER #####
    purchaseOrder = models.ManyToManyField(PurchaseOrder, blank = True)
    poitemsMerch = models.ManyToManyField(POItemsMerch, blank = True)
    poatc = models.ManyToManyField(POatc, blank=True)

    ##### RECEIVING REPORT #####
    receivingReport = models.ManyToManyField(ReceivingReport, blank = True)
    rritemsMerch = models.ManyToManyField(RRItemsMerch, blank = True)
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

    

    def __str__(self):
        return self.name