import string
from decimal import Decimal
import sweetify

def scChecker(request, sc):
    # INIT ERROR LIST
    err = []

    # GET MERCH INVENTORY WITH FOR LOOP
    for scitems in sc.scitemsmerch.all():
        inv = scitems.merchInventory

        # CHECK IF SCITEMS QTY < INV QTY
        if scitems.qty < inv.qtyA:
            err.append('Selling QTY < Inventory QTY')

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
