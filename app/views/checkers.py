import string
from decimal import Decimal
import sweetify
from ..models import WarehouseItems
import re 

def scVoidChecker(request, sc):
    # INIT ERROR LIST
    err = []

    # THERE ARE TWO VERSIONS OF SC
    # WITH SO AND W/O SO

    # REVERT QUANTITIES
    # IF NO SO
    if not sc.salesOrder:
        for element in sc.scitemsmerch.all():
            wi = WarehouseItems.objects.filter(merchInventory = element.merchInventory)[0]
            if not wi.salesWOSO(-element.qty):
                err.append('Error in reverting Sales Contract without sales order')

    # IF WITH SO
    else:
        for element in sc.scitemsmerch.all():
            wi = WarehouseItems.objects.filter(merchInventory = element.merchInventory)[0]
            if not wi.resQty(-element.qty):
                err.append('Error in reverting Sales Contract with sales order')


    # CHECK RELELVANT DCHILDACCOUNTS
    dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
    if not dChildAccount.otherIncome: err.append('Other Income Account missing')
    if not dChildAccount.outputVat: err.append('Output VAT Account missing')
    if not dChildAccount.cwit: err.append('Creditable Withholding Tax Account missing')


    if len(err):
        return err


    totalFees = Decimal(0)
    for fees in sc.scotherfees.all():
        totalFees += fees.fee

    journal = {
        'Debit': {
            'accounts': []
        },
        'Credit': {
            'accounts': []
        }
    }

    def customJeAPI(normally, account, amount):
        journal[normally]['accounts'].append({'name': account.name, 'amount': amount})

    customJeAPI('Debit', dChildAccount.otherIncome, totalFees)
    customJeAPI('Debit', dChildAccount.outputVat, sc.taxPeso)
    customJeAPI('Debit', dChildAccount.sales, sc.amountTotal - sc.taxPeso - totalFees)
    customJeAPI('Credit', sc.party.accountChild.get(name__regex=r"[Rr]eceivable"), sc.amountTotal)

    if sc.receivepayment.all():
        accountReceivable = Decimal(0.0)
        wep = Decimal(0.0)
        cashOnHand = Decimal(0.0)
        bankAccount = {}

        for rp in sc.receivepayment.all():
            accountReceivable += (rp.amountPaid + rp.wep)

            if rp.wep!= 0.0:
                wep += rp.wep

            if rp.paymentMethod == dChildAccount.cashOnHand.name:
                cashOnHand += rp.amountPaid

            elif re.search('[Cc]ash [Ii]n [Bb]ank', rp.paymentMethod):
                if rp.paymentMethod in bankAccount:
                    bankAccount[rp.paymentMethod] += rp.amountPaid
                else:
                    bankAccount[rp.paymentMethod] = rp.amountPaid

        customJeAPI('Debit', sc.party.accountChild.get(name__regex=r"[Rr]eceivable"), Decimal(accountReceivable))
        if wep != 0.0:
            customJeAPI('Credit', dChildAccount.cwit, Decimal(wep))
        
        if cashOnHand != 0.0:
            customJeAPI('Credit', dChildAccount.cashOnHand, Decimal(cashOnHand))

        for key, val in bankAccount.items():
            customJeAPI('Credit', dChildAccount.cashInBank.get(name=key), Decimal(val))

    sumDebit = sum(i['amount'] for i in journal['Debit']['accounts'])

    sumCredit = sum(i['amount'] for i in journal['Credit']['accounts'])

    if not round(sumDebit, 3) == round(sumCredit, 3):
        err.append('Journal did not balance')

    
    if len(err):
        return err
    else:
        return 0



def soChecker(request, so):
    #INIT ERROR LIST
    err = []

    for soitems in so.soitemsmerch.all():
        inv = soitems.merchInventory

        # CHECK IF SO ITEMS QTY > INV QTY
        if soitems.qty > inv.qtyA:
            err.append('Selling QTY > Inventory QTY')

        # CHECK IF RELELANT DCHILDACCOUNT HAS VALUE
        # SO DOESN'T HAVE JOURNAL 

    if len(err):
        return err
    else:
        return 0


def scChecker(request, sc):
    # INIT ERROR LIST
    err = []

    # GET MERCH INVENTORY WITH FOR LOOP
    for scitems in sc.scitemsmerch.all():
        inv = scitems.merchInventory

        # CHECK IF SCITEMS QTY > INV QTY
        if scitems.qty > inv.qtyA:
            err.append('Selling QTY > Inventory QTY')

    # CHECK IF RELEVANT DCHILDACCOUNT HAS VALUE
    dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

    if not dChildAccount.otherIncome: err.append('Other Income Account missing')
    if not dChildAccount.outputVat: err.append('Output VAT Account missing')

    for scitems in sc.scitemsmerch.all():
        if not scitems.merchInventory.childAccountSales: err.append('Item Sales Account missing')
        if not scitems.merchInventory.childAccountInventory: err.append('Item Inventory Account missing')
        if not scitems.merchInventory.childAccountCostOfSales: err.append('Item Cost of Sales Account Missing')
    
    if not sc.party.accountChild: err.append('Customer/Vendor Account missing')


    totalFees = Decimal(0)
    for fees in sc.scotherfees.all():
        totalFees += fees.fee

    journal = {
        'Debit': {
            'accounts': []
        },
        'Credit': {
            'accounts': []
        }
    }

    if len(err):
        return err

    def customJeAPI(normally, account, amount):
        journal[normally]['accounts'].append({'name': account.name, 'amount': amount})

    customJeAPI('Credit', dChildAccount.otherIncome, totalFees)
    customJeAPI('Credit', dChildAccount.outputVat, sc.taxPeso)
    for item in sc.scitemsmerch.all():
        customJeAPI('Credit', item.merchInventory.childAccountSales, (item.totalCost)-(sc.discountPeso/sc.scitemsmerch.all().count())-(item.totalCost*(sc.taxRate/100)))
    for element in sc.scitemsmerch.all():
        customJeAPI('Credit', element.merchInventory.childAccountInventory, element.merchInventory.purchasingPrice*element.qty)
    for element in sc.scitemsmerch.all():
        customJeAPI('Debit', element.merchInventory.childAccountCostOfSales, element.merchInventory.purchasingPrice*element.qty)
    customJeAPI('Debit', sc.party.accountChild.get(name__regex=r"[Rr]eceivable"), sc.amountTotal) 

    sumDebit = sum(i['amount'] for i in journal['Debit']['accounts'])

    sumCredit = sum(i['amount'] for i in journal['Credit']['accounts'])

    if not round(sumDebit, 3) == round(sumCredit, 3):
        err.append('Journal did not balance')

    
    if len(err):
        return err
    else:
        return 0
