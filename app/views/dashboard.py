import sweetify
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *
from decimal import Decimal
from time import sleep
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class DashboardView(View):
    def get(self, request):
        if request.user.authLevel == '0':
            return redirect('/admin-dashboard/')
        context = {
            'branches': Branch.objects.all()
        }
        return render(request, 'dashboard.html', context)

class AdminDashboardView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == "1":
            raise PermissionDenied()
        context = {
            'branches': Branch.objects.all()
        }
        return render(request, 'admin-dashboard.html', context)

class AdminChangeUserBranch(APIView):
    def post(self, request):
        user = request.user
        data = request.data

        user.branch = Branch.objects.get(pk=data['branch'])
        user.save()

        sleep(.5)

        return JsonResponse(0, safe=False)

class SaveNotepad(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.get(pk=data['userID'])
        print(data)
        try:
            user.notepad.notes = data['notepad']
            user.notepad.save()
        except:
            notepad = Notepad()
            notepad.user = user
            notepad.notes = data['notepad']
            notepad.save()
        
        return JsonResponse(0, safe=False)

class SaveAnnouncement(APIView):
    def post(self, request):
        data = request.data
        announce = Announcement()

        announce.title = data['title']
        announce.contents = data['contents']
        announce.branch = request.user.branch

        announce.save()

        notify(request, 'New Announcement', '', '/dashboard/', 1)

        return JsonResponse(0, safe=False)

class DeleteAnnouncement(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == "1":
            raise PermissionDenied()
        data= request.data
        Announcement.objects.get(pk=data['id']).delete()

        return JsonResponse(0, safe=False)

class CreateBranchInDashboard(APIView):
    def post(self, request, format=None):
        branch = request.data

        if not branch['branchName']:
            return JsonResponse(1, safe=False)

        bdca = BranchDefaultChildAccount()
        bdca.save()

        bp = BranchProfile()
        bp.branchDefaultChildAccount = bdca
        bp.save()

        b = Branch()
        b.name = branch['branchName']
        b.branchProfile = bp
        b.save()

        request.user.branch = b
        request.user.save()


        # ACCOUNT GROUP
        # request.user.branch.accountGroup.add()
        currentAsset = AccountGroup(code="##", name="Current Assets", normally="Debit", permanence="Real", amount=Decimal(0))
        currentAsset.save()
        request.user.branch.accountGroup.add(currentAsset)

        nonCurrentAsset = AccountGroup(code="##", name="Non-Current Assets", normally="Debit", permanence="Real", amount=Decimal(0))
        nonCurrentAsset.save()
        request.user.branch.accountGroup.add(nonCurrentAsset)

        currentLiabilities = AccountGroup(code="##", name="Current Liabilities", normally="Credit", permanence="Real", amount=Decimal(0))
        currentLiabilities.save()
        request.user.branch.accountGroup.add(currentLiabilities)

        nonCurrentLiabilites = AccountGroup(code="##", name="Non-Current Liabilities", normally="Credit", permanence="Real", amount=Decimal(0))
        nonCurrentLiabilites.save()
        request.user.branch.accountGroup.add(nonCurrentLiabilites)

        equity = AccountGroup(code="##", name="Equity", normally="Credit", permanence="Real", amount=Decimal(0))
        equity.save()
        request.user.branch.accountGroup.add(equity)
        
        revenue = AccountGroup(code="##", name="Revenue", normally="Credit", permanence="Nominal", amount=Decimal(0))
        revenue.save()
        request.user.branch.accountGroup.add(revenue)

        costOfSales = AccountGroup(code="##", name="Cost of Sales", normally="Credit", permanence="Nominal", amount=Decimal(0))
        costOfSales.save()
        request.user.branch.accountGroup.add(costOfSales)

        sales = AccountGroup(code="##", name="Sales", normally="Credit", permanence='Real', amount=Decimal(0))
        sales.save()
        request.user.branch.accountGroup.add(sales)

        operatingExpense = AccountGroup(code="##", name="Operating Expense", normally="Credit", permanence="Nominal", amount=Decimal(0))
        operatingExpense.save()
        request.user.branch.accountGroup.add(operatingExpense)

        adminExpense = AccountGroup(code="##", name="Administrative Expense", normally="Credit", permanence="Nominal", amount=Decimal(0))
        adminExpense.save()
        request.user.branch.accountGroup.add(adminExpense)

        otherIncome = AccountGroup(code="##", name="Other Income", normally="Credit", permanence="Real", amount=Decimal(0))
        otherIncome.save()
        request.user.branch.accountGroup.add(otherIncome)

        otherLoss = AccountGroup(code="##", name="Other Losses", normally="Credit", permanence="Real", amount=Decimal(0))
        otherLoss.save()
        request.user.branch.accountGroup.add(otherLoss)
        
        # SUB GROUP
        costOfSalesSubGroup = AccountSubGroup(code="##", name="Cost of Sales", accountGroup=costOfSales, amount=Decimal(0))
        costOfSalesSubGroup.save()
        request.user.branch.subGroup.add(costOfSalesSubGroup)

        cash = AccountSubGroup(code="##", name="Cash", accountGroup=currentAsset, amount=Decimal(0))
        cash.save()
        request.user.branch.subGroup.add(cash)
        
        inventory = AccountSubGroup(code="##", name="Inventory", accountGroup=currentAsset, amount=Decimal(0))
        inventory.save()
        request.user.branch.subGroup.add(inventory)
        
        accountsReceivable = AccountSubGroup(code="##", name="Accounts Receivable", accountGroup=currentAsset, amount=Decimal(0))
        accountsReceivable.save()
        request.user.branch.subGroup.add(accountsReceivable)

        otherCurrentAsset = AccountSubGroup(code="##", name="Other Current Asset", accountGroup=currentAsset, amount=Decimal(0))
        otherCurrentAsset.save()
        request.user.branch.subGroup.add(otherCurrentAsset)

        accountsPayables = AccountSubGroup(code="##", name="Accounts Payables", accountGroup=currentLiabilities, amount=Decimal(0))
        accountsPayables.save()
        request.user.branch.subGroup.add(accountsPayables)

        shareCapital = AccountSubGroup(code="##", name="Share Capital", accountGroup=equity, amount=Decimal(0))
        shareCapital.save()
        request.user.branch.subGroup.add(shareCapital)

        salesSubGroup = AccountSubGroup(code="##", name="Sales", accountGroup=sales, amount=Decimal(0))
        salesSubGroup.save()
        request.user.branch.subGroup.add(salesSubGroup)

        paidCapital = AccountSubGroup(code="##", name="Paid Capital", accountGroup=equity, amount=Decimal(0))
        paidCapital.save()
        request.user.branch.subGroup.add(paidCapital)

        retainedEarning = AccountSubGroup(code="##", name="Retained Earnings", accountGroup=equity, amount=Decimal(0))
        retainedEarning.save()
        request.user.branch.subGroup.add(retainedEarning)

        operatingExpenseSubGroup = AccountSubGroup(code="##", name="Operating Expense", accountGroup=operatingExpense, amount=Decimal(0))
        operatingExpenseSubGroup.save()
        request.user.branch.subGroup.add(operatingExpenseSubGroup)

        adminExpenseSubGroup = AccountSubGroup(code="##", name="Administrative Expense", accountGroup=adminExpense, amount=Decimal(0))
        adminExpenseSubGroup.save()
        request.user.branch.subGroup.add(adminExpenseSubGroup)

        otherLossSubGroup = AccountSubGroup(code="##", name="Other Losses", accountGroup=otherLoss, amount=Decimal(0))
        otherLossSubGroup.save()
        request.user.branch.subGroup.add(otherLossSubGroup)


        # CHILD ACCOUNT GROUP
        costOfSalesChild = AccountChild(code="##", name="Cost of Sales", accountSubGroup=costOfSalesSubGroup, amount=Decimal(0))
        costOfSalesChild.save()
        request.user.branch.accountChild.add(costOfSalesChild)
        bdca.costOfSales = costOfSalesChild
        bdca.save()

        cashOnHand = AccountChild(code="##", name="Cash on Hand", accountSubGroup=cash, amount=Decimal(0))
        cashOnHand.save()
        request.user.branch.accountChild.add(cashOnHand)
        bdca.cashOnHand = cashOnHand
        bdca.save()

        cashInBank = AccountChild(code="##", name="Cash in Bank", accountSubGroup=cash, amount=Decimal(0))
        cashInBank.save()
        request.user.branch.accountChild.add(cashInBank)
        bdca.cashInBank.add(cashInBank)
        bdca.save()

        pettyCash = AccountChild(code="##", name="Petty Cash", accountSubGroup=cash, amount=Decimal(0))
        pettyCash.save()
        request.user.branch.accountChild.add(pettyCash)
        bdca.pettyCash = pettyCash
        bdca.save()

        merchInventory = AccountChild(code="##", name="Merchandise Inventory", accountSubGroup=inventory, amount=Decimal(0))
        merchInventory.save()
        request.user.branch.accountChild.add(merchInventory)
        bdca.merchInventory = merchInventory
        bdca.save()

        tradeReceivable = AccountChild(code="##", name="Trade Receivable", accountSubGroup=accountsReceivable, amount=Decimal(0))
        tradeReceivable.save()
        request.user.branch.accountChild.add(tradeReceivable)
        

        prepaidExpense = AccountChild(code="##", name="Prepaid Expense", accountSubGroup=otherCurrentAsset, amount=Decimal(0))
        prepaidExpense.save()
        request.user.branch.accountChild.add(prepaidExpense)
        bdca.prepaidExpense = prepaidExpense
        bdca.save()

        inputVAT = AccountChild(code="##", name="Input VAT", accountSubGroup=otherCurrentAsset, amount=Decimal(0))
        inputVAT.save()
        request.user.branch.accountChild.add(inputVAT)
        bdca.inputVat = inputVAT
        bdca.save()

        cwit = AccountChild(code="##", name="Creditable Withholding Income Tax", accountSubGroup=otherCurrentAsset, amount=Decimal(0))
        cwit.save()
        request.user.branch.accountChild.add(cwit)
        bdca.cwit = cwit
        bdca.save()

        tradePayables = AccountChild(code="##", name="Trade Payables", accountSubGroup=accountsPayables, amount=Decimal(0))
        tradePayables.save()
        request.user.branch.accountChild.add(tradePayables)

        wep = AccountChild(code="##", name="Withholding Expanded Payables", accountSubGroup=accountsPayables, amount=Decimal(0))
        wep.save()
        request.user.branch.accountChild.add(wep)
        bdca.ewp = wep
        bdca.save()

        outputVATPayables = AccountChild(code="##", name="Output VAT Payables", accountSubGroup=accountsPayables, amount=Decimal(0))
        outputVATPayables.save()
        request.user.branch.accountChild.add(outputVATPayables)
        bdca.outputVat = outputVATPayables
        bdca.save()

        advancesToSupplier = AccountChild(code="##", name="Advances to Supplier", accountSubGroup=accountsReceivable, amount=Decimal(0))
        advancesToSupplier.save()
        request.user.branch.accountChild.add(advancesToSupplier)
        bdca.advancesToSupplier.add(advancesToSupplier)
        bdca.save()
        
        sales = AccountChild(code="##", name = "Sales", accountSubGroup = salesSubGroup, amount=Decimal(0))
        sales.save()
        request.user.branch.accountChild.add(sales)
        bdca.sales = sales
        bdca.save()

        salariesExpense = AccountChild(code="##", name = "Salaries Expense", accountSubGroup = operatingExpenseSubGroup , amount = Decimal(0))
        salariesExpense.save()
        request.user.branch.accountChild.add(salariesExpense)
        bdca.salariesExpense = salariesExpense
        bdca.save()
        
        bonus = AccountChild(code="##", name = "Bonuses", accountSubGroup = operatingExpenseSubGroup , amount = Decimal(0))
        bonus.save()
        request.user.branch.accountChild.add(bonus)
        bdca.bonus = bonus
        bdca.save()
        
        deminimisBenefits = AccountChild(code="##", name = "Deminimis Benefits", accountSubGroup = operatingExpenseSubGroup , amount = Decimal(0))
        deminimisBenefits.save()
        request.user.branch.accountChild.add(deminimisBenefits)
        bdca.deminimisBenefit = deminimisBenefits
        bdca.save()

        hdmfShare = AccountChild(code="##", name = "HDMF Share", accountSubGroup = operatingExpenseSubGroup , amount = Decimal(0))
        hdmfShare.save()
        request.user.branch.accountChild.add(hdmfShare)
        bdca.hdmfShare = hdmfShare
        bdca.save()

        phicERShare = AccountChild(code="##", name = "PHIC ER Share", accountSubGroup = operatingExpenseSubGroup , amount = Decimal(0))
        phicERShare.save()
        request.user.branch.accountChild.add(phicERShare)
        bdca.phicERShare = phicERShare
        bdca.save()

        sssERShare = AccountChild(code="##", name = "SSS ER Share", accountSubGroup = operatingExpenseSubGroup , amount = Decimal(0))
        sssERShare.save()
        request.user.branch.accountChild.add(sssERShare)
        bdca.sssERShare = sssERShare
        bdca.save()

        salariesPayable = AccountChild(code="##", name = "Salaries Payable", accountSubGroup = accountsPayables , amount = Decimal(0))
        salariesPayable.save()
        request.user.branch.accountChild.add(salariesPayable)
        bdca.salariesPayable = salariesPayable
        bdca.save()

        sssPayable = AccountChild(code="##", name = "SSS Payable", accountSubGroup = accountsPayables , amount = Decimal(0))
        sssPayable.save()
        request.user.branch.accountChild.add(sssPayable)
        bdca.sssPayable = sssPayable
        bdca.save()

        phicPayable = AccountChild(code="##", name = "PHIC Payable", accountSubGroup = accountsPayables , amount = Decimal(0))
        phicPayable.save()
        request.user.branch.accountChild.add(phicPayable)
        bdca.phicPayable = phicPayable
        bdca.save()
        
        hdmfPayable = AccountChild(code="##", name = "HDMF Payable", accountSubGroup = accountsPayables , amount = Decimal(0))
        hdmfPayable.save()
        request.user.branch.accountChild.add(hdmfPayable)
        bdca.hdmfPayable = hdmfPayable
        bdca.save()

        withholdingTaxPayable = AccountChild(code="##", name = "Withholding Tax Payable", accountSubGroup = accountsPayables , amount = Decimal(0))
        withholdingTaxPayable.save()
        request.user.branch.accountChild.add(withholdingTaxPayable)
        bdca.withholdingTaxPayable = withholdingTaxPayable
        bdca.save()

        childShareCapital = AccountChild(code="##", name="Share Capital", accountSubGroup=shareCapital, amount=Decimal(0))
        childShareCapital.save()
        request.user.branch.accountChild.add(childShareCapital)

        childPaidCapital = AccountChild(code="##", name="Paid Capital", accountSubGroup=paidCapital, amount=Decimal(0))
        childPaidCapital.save()
        request.user.branch.accountChild.add(childPaidCapital)

        childRetainedEarning = AccountChild(code="##", name="Retained Earnings", accountSubGroup=retainedEarning, amount=Decimal(0))
        childRetainedEarning.save()
        request.user.branch.accountChild.add(childRetainedEarning)

        advancesToEmployee = AccountChild(code="##", name="Advances to Employee", accountSubGroup=accountsReceivable, amount=Decimal(0))
        advancesToEmployee.save()
        request.user.branch.accountChild.add(advancesToEmployee)

        laborExpense = AccountChild(code="##", name="Labor Expense", accountSubGroup=operatingExpenseSubGroup, amount=Decimal(0))
        laborExpense.save()
        request.user.branch.accountChild.add(laborExpense)
        bdca.laborExpense = laborExpense
        bdca.save()

        workInProgress = AccountChild(code="##", name="Work in Progress", accountSubGroup=inventory, amount=Decimal(0))
        workInProgress.save()
        request.user.branch.accountChild.add(workInProgress)
        bdca.workInProgress = workInProgress
        bdca.save()

        factorySupplies = AccountChild(code="##", name="Factory Supplies", accountSubGroup=operatingExpenseSubGroup, amount=Decimal(0))
        factorySupplies.save()
        request.user.branch.accountChild.add(factorySupplies)
        bdca.factorySupplies = factorySupplies
        bdca.save()



        ####### THIS CODE NEEDS SOME CHECKING #######
        materialLosses = AccountChild(code="##", name="Material Losses", accountSubGroup=otherLossSubGroup, amount=Decimal(0))
        materialLosses.save()
        request.user.branch.accountChild.add(materialLosses)
        bdca.materialLosses = materialLosses
        bdca.save()
        ####### END #######


        


        notify(request, 'New Branch/Company', f'{b.name} has been created', '/dashboard/', 0)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ConnectBranchInDashboard(APIView):
    def post(self, request, format=None):
        branch = request.data

        request.user.branch = Branch.objects.get(pk=branch['branchID'])
        request.user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)