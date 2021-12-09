import sweetify
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *
from decimal import Decimal

class DashboardView(View):
    def get(self, request):
        context = {
            'branches': Branch.objects.all(),
            "revenue": request.user.branch.accountGroup.get(name__regex=r'[Rr]evenue')
        }
        return render(request, 'dashboard.html', context)

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

class CreateBranchInDashboard(APIView):
    def post(self, request, format=None):
        branch = request.data

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

        genExp = AccountGroup(code="##", name="General Expense", normally="Credit", permanence="Nominal", amount=Decimal(0))
        genExp.save()
        request.user.branch.accountGroup.add(genExp)

        otherIncome = AccountGroup(code="##", name="Other Income", normally="Credit", permanence="Real", amount=Decimal(0))
        otherIncome.save()
        request.user.branch.accountGroup.add(otherIncome)

        otherLoss = AccountGroup(code="##", name="Other Lose", normally="Credit", permanence="Real", amount=Decimal(0))
        otherLoss.save()
        request.user.branch.accountGroup.add(otherLoss)
        
        # SUB GROUP
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

        paidCapital = AccountSubGroup(code="##", name="Paid Capital", accountGroup=equity, amount=Decimal(0))
        paidCapital.save()
        request.user.branch.subGroup.add(paidCapital)

        retainedEarning = AccountSubGroup(code="##", name="Retained Earnings", accountGroup=equity, amount=Decimal(0))
        retainedEarning.save()
        request.user.branch.subGroup.add(retainedEarning)


        # CHILD ACCOUNT GROUP
        cashOnHand = AccountChild(code="##", name="Cash on Hand", accountSubGroup=cash, amount=Decimal(0))
        cashOnHand.save()
        request.user.branch.accountChild.add(cashOnHand)

        cashInBank = AccountChild(code="##", name="Cash in Bank", accountSubGroup=cash, amount=Decimal(0))
        cashInBank.save()
        request.user.branch.accountChild.add(cashInBank)

        merchInventory = AccountChild(code="##", name="Merchandise Inventory", accountSubGroup=inventory, amount=Decimal(0))
        merchInventory.save()
        request.user.branch.accountChild.add(merchInventory)

        tradeReceivable = AccountChild(code="##", name="Trade Receivable", accountSubGroup=accountsReceivable, amount=Decimal(0))
        tradeReceivable.save()
        request.user.branch.accountChild.add(tradeReceivable)

        prepaidExpense = AccountChild(code="##", name="Prepaid Expense", accountSubGroup=otherCurrentAsset, amount=Decimal(0))
        prepaidExpense.save()
        request.user.branch.accountChild.add(prepaidExpense)

        inputVAT = AccountChild(code="##", name="Input VAT", accountSubGroup=otherCurrentAsset, amount=Decimal(0))
        inputVAT.save()
        request.user.branch.accountChild.add(inputVAT)

        cwit = AccountChild(code="##", name="Creditable Withholding Income Tax", accountSubGroup=otherCurrentAsset, amount=Decimal(0))
        cwit.save()
        request.user.branch.accountChild.add(cwit)

        tradePayables = AccountChild(code="##", name="Trade Payables", accountSubGroup=accountsPayables, amount=Decimal(0))
        tradePayables.save()
        request.user.branch.accountChild.add(tradePayables)

        wep = AccountChild(code="##", name="Withholding Expanded Payables", accountSubGroup=accountsPayables, amount=Decimal(0))
        wep.save()
        request.user.branch.accountChild.add(wep)

        outputVATPayables = AccountChild(code="##", name="Output VAT Payables", accountSubGroup=accountsPayables, amount=Decimal(0))
        outputVATPayables.save()
        request.user.branch.accountChild.add(outputVATPayables)

        childShareCapital = AccountChild(code="##", name="Share Capital", accountSubGroup=shareCapital, amount=Decimal(0))
        childShareCapital.save()
        request.user.branch.accountChild.add(childShareCapital)

        childPaidCapital = AccountChild(code="##", name="Paid Capital", accountSubGroup=paidCapital, amount=Decimal(0))
        childPaidCapital.save()
        request.user.branch.accountChild.add(childPaidCapital)

        childRetainedEarning = AccountChild(code="##", name="Retained Earnings", accountSubGroup=retainedEarning, amount=Decimal(0))
        childRetainedEarning.save()
        request.user.branch.accountChild.add(childRetainedEarning)



        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class ConnectBranchInDashboard(APIView):
    def post(self, request, format=None):
        branch = request.data

        request.user.branch = Branch.objects.get(pk=branch['branchID'])
        request.user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)