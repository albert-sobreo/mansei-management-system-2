import string
from decimal import Decimal
import sweetify
from ..models import WarehouseItems
import re 
import pprint
import copy

##### THIS CHECKER IS OBSOLETE ######
def pvPoMerchChecker(request, voucher):
    # INIT ERR
    err = []
    dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

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

    if voucher.purchaseOrder.runningBalance == voucher.purchaseOrder.amountTotal:
        ################# IF RR WAS DONE BEFORE PV #################
        if voucher.purchaseOrder.receivingreport.first():
            ################# IF RR IS APPROVED #################
            if voucher.purchaseOrder.receivingreport.first().approved == True:
                customJeAPI('Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
            ################# IF RR IS NOT APPROVED UPON PV #################
            else:
                customJeAPI('Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)
                customJeAPI('Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))
        ################# IF PV IS DONE BEFORE RR #################
        else:
            customJeAPI('Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)
            customJeAPI('Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))
    ################# IF NOT FIRST PAYMENT #################
    else:
        customJeAPI('Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
    voucher.purchaseOrder.wep += voucher.wep
    ################# CREDIT SIDE #################
    customJeAPI('Credit', dChildAccount.ewp, voucher.wep)
    if voucher.paymentPeriod == 'Full Payment':
        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
            customJeAPI('Credit', dChildAccount.cashOnHand, voucher.amountPaid)
            
        elif voucher.paymentMethod == dChildAccount.pettyCash.name:
            customJeAPI('Credit', dChildAccount.pettyCash, voucher.amountPaid)
        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
            customJeAPI('Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
        elif voucher.paymentMethod == "Cheque":
            customJeAPI('Credit', voucher.cheque.accountChild, voucher.amountPaid)
            
    elif voucher.paymentPeriod == 'Partial Payment':
        print('b0ss plis')
        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
            customJeAPI('Credit', dChildAccount.cashOnHand, voucher.amountPaid)
            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
        elif voucher.paymentMethod == dChildAccount.pettyCash.name:
            customJeAPI('Credit', dChildAccount.pettyCash, voucher.amountPaid)
            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
            customJeAPI('Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
        elif voucher.paymentMethod == "Cheque":
            customJeAPI('Credit', voucher.cheque.accountChild, voucher.amountPaid)
            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
    if voucher.paymentMethod == "Memorandum":
        if voucher.purchaseOrder.runningBalance <= voucher.amountPaid:
            customJeAPI('Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.purchaseOrder.runningBalance)
        else:
            customJeAPI('Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.amountPaid)
            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

    sumDebit = sum(i['amount'] for i in journal['Debit']['accounts'])

    sumCredit = sum(i['amount'] for i in journal['Credit']['accounts'])

    if not round(sumDebit, 3) == round(sumCredit, 3):
        err.append('Journal did not balance')

    
    if len(err):
        return err
    else:
        return 0


def scVoidChecker(request, salesContract):
    sc = copy.deepcopy(salesContract)
    # INIT ERROR LIST
    err = []

    # THERE ARE TWO VERSIONS OF SC
    # WITH SO AND W/O SO

    # REVERT QUANTITIES

    # NO SALES ORDER
    if not sc.salesOrder:
        for element in sc.scitemsmerch.all():
            wi = WarehouseItems.objects.filter(merchInventory = element.merchInventory)[0]
            if not wi.salesWOSO(-element.qty):
                err.append('Error in reverting Sales Contract without sales order')

    # WITH SALES ORDER
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


def scChecker(request, salesContract):
    sc = copy.deepcopy(salesContract)
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
        customJeAPI('Credit', item.merchInventory.childAccountSales, (item.totalCost)-(sc.discountPeso/sc.scitemsmerch.all().count())-((item.totalCost-(sc.discountPeso/sc.scitemsmerch.all().count()))*(sc.taxRate/100)))
        print(item.totalCost, sc.discountPeso/sc.scitemsmerch.all().count(), item.totalCost*(sc.taxRate/100))
    
    
    for element in sc.scitemsmerch.all():
        customJeAPI('Credit', element.merchInventory.childAccountInventory, element.merchInventory.purchasingPrice*element.qty)
    
    
    for element in sc.scitemsmerch.all():
        customJeAPI('Debit', element.merchInventory.childAccountCostOfSales, element.merchInventory.purchasingPrice*element.qty)
    
    
    customJeAPI('Debit', sc.party.accountChild.get(name__regex=r"[Rr]eceivable"), sc.amountTotal) 

    pprint.pprint(journal)

    
    sumDebit = sum(i['amount'] for i in journal['Debit']['accounts'])

    sumCredit = sum(i['amount'] for i in journal['Credit']['accounts'])

    if not round(sumDebit, 3) == round(sumCredit, 3):
        err.append('Journal did not balance')

    
    if len(err):
        return err
    else:
        return 0


def pvPOMerchChecker(request, pv):
    voucher = copy.deepcopy(pv)
    # INIT ERROR LIST
    err = []

    # CHECK IF RELEVANT DCHILDACCOUNT HAS VALUE
    dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

    if not dChildAccount.inputVat: err.append('inputVat Account missing')
    if not dChildAccount.prepaidExpense: err.append('prepaidExpense Account missing')
    if not dChildAccount.ewp: err.append('ewp Account missing')
    if not dChildAccount.cashOnHand: err.append('cashOnHand Account missing')
    if not dChildAccount.pettyCash: err.append('pettyCash Account missing')

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



    ########################################
    ########## TESTING OF JOURNAL ##########
    ########################################


    ################# DEBIT SIDE #################
    ################# IF FIRST PAYMENT #################
    if voucher.purchaseOrder.runningBalance == voucher.purchaseOrder.amountTotal:
        ################# IF RR WAS DONE BEFORE PV #################
        if voucher.purchaseOrder.receivingreport.first():
            ################# IF RR IS APPROVED #################
            if voucher.purchaseOrder.receivingreport.first().approved == True:

                customJeAPI('Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
            ################# IF RR IS NOT APPROVED UPON PV #################
            else:
                customJeAPI('Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

                customJeAPI('Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))

        ################# IF PV IS DONE BEFORE RR #################
        else:
            customJeAPI('Debit', dChildAccount.inputVat, voucher.purchaseOrder.taxPeso)

            customJeAPI('Debit', dChildAccount.prepaidExpense, (voucher.purchaseOrder.amountDue - voucher.purchaseOrder.taxPeso))

    ################# IF NOT FIRST PAYMENT #################
    else:
        customJeAPI('Debit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))


    ### I DUNNO WHATS THIS FOR ###
    voucher.purchaseOrder.wep += voucher.wep
    customJeAPI('Credit', dChildAccount.ewp, voucher.wep)


    if voucher.paymentPeriod == 'Full Payment':
        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
            customJeAPI('Credit', dChildAccount.cashOnHand, voucher.amountPaid)

            
        elif voucher.paymentMethod == dChildAccount.pettyCash.name:
            customJeAPI('Credit', dChildAccount.pettyCash, voucher.amountPaid)

        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
            customJeAPI('Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)
        elif voucher.paymentMethod == "Cheque":
            customJeAPI('Credit', voucher.cheque.accountChild, voucher.amountPaid)
            
    elif voucher.paymentPeriod == 'Partial Payment':
        print('b0ss plis')
        if voucher.paymentMethod == dChildAccount.cashOnHand.name:
            customJeAPI('Credit', dChildAccount.cashOnHand, voucher.amountPaid)

            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

        elif voucher.paymentMethod == dChildAccount.pettyCash.name:
            customJeAPI('Credit', dChildAccount.pettyCash, voucher.amountPaid)

            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

        elif re.search('[Cc]ash [Ii]n [Bb]ank', voucher.paymentMethod):
            customJeAPI('Credit', dChildAccount.cashInBank.get(name=voucher.paymentMethod), voucher.amountPaid)

            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
        elif voucher.paymentMethod == "Cheque":
            customJeAPI('Credit', voucher.cheque.accountChild, voucher.amountPaid)

            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))
    if voucher.paymentMethod == "Memorandum":
        if voucher.purchaseOrder.runningBalance <= voucher.amountPaid:
            customJeAPI('Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.purchaseOrder.runningBalance)
        else:
            customJeAPI('Credit', voucher.transaction.party.accountChild.get(name__regex=r"[Rr]eceivable"), voucher.amountPaid)
            customJeAPI('Credit', voucher.purchaseOrder.party.accountChild.get(name__regex=r"[Pp]ayable"), ((voucher.purchaseOrder.runningBalance - voucher.amountPaid) + (voucher.purchaseOrder.poatc.first().amountWithheld - voucher.purchaseOrder.wep)))

    pprint.pprint(journal)
    
    sumDebit = sum(i['amount'] for i in journal['Debit']['accounts'])

    sumCredit = sum(i['amount'] for i in journal['Credit']['accounts'])

    if not round(sumDebit, 3) == round(sumCredit, 3):
        err.append('Journal did not balance')

    
    if len(err):
        return err
    else:
        return 0
