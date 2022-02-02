from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
import datetime
from django.core.exceptions import PermissionDenied
from decimal import Decimal
from .journalAPI import jeAPI

class JobOrderView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        user = request.user

        try:
            jo = user.branch.jobOrder.latest('pk')

            listed_code = jo.code.split('-')
            listed_date = str(datetime.date.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'JO-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'JO-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(datetime.date.today()).split('-')
            new_code = 'JO-{}-{}-0001'.format(listed_date[0], listed_date[1])

        operationalExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Oo]peration")
        administrativeExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Aa]dmin")

        try:
            directLabor = request.user.branch.branchProfile.branchDefaultChildAccount.laborExpense
        except Exception as e:
            print(e)
            directLabor = {'pk': None, 'name': 'Connect Labor Expense first in Branch profile'}
        
        fact = request.user.branch.branchProfile.branchDefaultChildAccount.factorySupplies
        context = {
            'new_code': new_code,
            'operational': operationalExpenses,
            'administrative': administrativeExpenses,
            'directLabor': directLabor,
            'factorySupplies': fact,
        }    
        return render(request, 'job-order.html', context)

class CreateJobOrderAPI(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        jo = JobOrder()

        jo.code = request.data['code']
        jo.datetimeCreated = datetime.datetime.now()
        jo.jobOrderCost = request.data['jobOrderCost']
        jo.method = request.data['method']
        jo.save()
        request.user.branch.jobOrder.add(jo)
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        if request.user.is_authenticated:
            jo.createdBy = request.user
            jo.save()

        for item in request.data['rawmaterials']:
            rawMat = RawMaterials()
            try:
                rawMat.merchInventory = MerchandiseInventory.objects.get(pk=item['merchInventory'])
            except Exception as e:
                print(e)
                rawMat.merchInventory = None
            rawMat.jobOrder = jo
            rawMat.qty = item['qty']
            rawMat.remaining = item['remaining']
            rawMat.merchInventory.warehouseitems.all()[0].addQty(-(item['qty'])) 
            rawMat.merchInventory.warehouseitems.all()[0].save2()
            rawMat.purchasingPrice = item['purchasingPrice']
            rawMat.totalCost = item['totalCost']
            rawMat.save()
            request.user.branch.rawMaterials.add(rawMat)

        for item in request.data['overheadexpenses']:
            ov = OverheadExpenses()
            try:
                ov.expenses = AccountChild.objects.get(pk=item['expenses'])
            except Exception as e:
                ov.expenses = None
            ov.cost = item['cost']
            ov.jobOrder = jo
            ov.save()
            request.user.branch.overheadExpenses.add(ov)

        for item in request.data['directlabor']:
            dl = DirectLabor()
            try:
                dl.expenses = AccountChild.objects.get(pk=item['expenses'])
            except Exception as e:
                print(e)
                dl.expenses = None
            dl.cost = item['cost']
            dl.jobOrder = jo
            dl.save()
            request.user.branch.directLabor.add(dl)

        for item in request.data['finalproduct']:
            finalProduct = FinalProduct()
            finalProduct.name = item['name']
            finalProduct.qty = item['qty']
            finalProduct.unitCost = item['unitCost']
            finalProduct.totalCost = item['totalCost']
            finalProduct.jobOrder = jo
            finalProduct.save()
            request.user.branch.finalProduct.add(finalProduct)

        for item in request.data['materiallosses']:
            losses = MaterialLosses()
            losses.name = item['name']
            losses.qty = item['qty']
            losses.unitCost = item['unitCost']
            losses.totalCost = item['totalCost']
            losses.jobOrder = jo
            losses.save()
            request.user.branch.materialLosses.add(losses)
        

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

        

class JobOrderOnGoingView(View):
    def get(self, request):
        context = {
            'jos': request.user.branch.jobOrder.filter(status='on-going')
        }
        return render(request, 'job-order-ongoing.html', context)

class JobOrderFinishedView(View):
    def get(self, request):
        context = {
            'jos': request.user.branch.jobOrder.filter(status='finished')
        }
        return render(request, 'job-order-finished.html', context)

class EditJobOrderView(View):
    def get(self, request):
        if request.user.authLevel=='2':
            raise PermissionDenied()

        operationalExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Oo]peration")
        administrativeExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Aa]dmin")

        context = {
            'jos': request.user.branch.jobOrder.exclude(status='finished'),
            'operational': operationalExpenses,
            'administrative': administrativeExpenses
        }

        return render(request, 'job-order-edit-on-going.html', context)

class EditJobOrder(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        oldJO = JobOrder.objects.get(pk=request.data['id'])
        newJO = request.data

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        j = Journal()

        j.code = oldJO.code
        j.datetimeCreated = oldJO.datetimeCreated
        j.createdBy = oldJO.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)

        rawmat = Decimal(0)
        # for item in request.data['rawmaterials']:
        #     if item['merchInventory']:
        #         rawMat = RawMaterials()
        #         rawMat.merchInventory = MerchandiseInventory.objects.get(pk=item['merchInventory'])
        #         rawMat.jobOrder = jo
        #         rawMat.qty = item['qty']
        #         rawMat.remaining = item['remaining']
        #         rawMat.purchasingPrice = item['purchasingPrice']
        #         rawMat.totalCost = item['totalCost']
        #         rawMat.save()
        #         request.user.branch.rawMaterials.add(rawMat)
        #         rawmat += rawMat.totalCost

        newRawMatIDS = []
        for item in newJO['rawmaterials']:
            if oldJO.rawmaterials.filter(pk=item['id']):
                oldRawmat = oldJO.rawmaterials.filter(pk=item['id'])[0]
                diff = Decimal(0)
                if oldRawmat.qty < Decimal(item['qty']):
                    diff = abs(oldRawmat.qty - Decimal(item['qty']))
                    oldRawmat.qty +=  diff
                    oldRawmat.remaining += diff
                    oldRawmat.merchInventory.warehouseitems.all()[0].addQty((item['qty'])) 
                    oldRawmat.merchInventory.warehouseitems.all()[0].save2()
                    oldRawmat.totalCost = item['totalCost']
                    oldRawmat.merchInventory.save()
                    oldRawmat.save()
                elif oldRawmat.qty > item['qty']:
                    diff = abs(Decimal(item['qty']) - oldRawmat.qty)
                    oldRawmat.qty -=  diff
                    oldRawmat.remaining -= diff
                    oldRawmat.merchInventory.warehouseitems.all()[0].addQty(-(item['qty'])) 
                    oldRawmat.merchInventory.warehouseitems.all()[0].save2()
                    oldRawmat.totalCost = item['totalCost']
                    oldRawmat.merchInventory.save()
                    oldRawmat.save()


            else:
                newRawMatIDS.append(item['id'])
                newRawmat = RawMaterials()
                newRawmat.merchInventory = MerchandiseInventory.objects.get(pk=item['merchInventory'])
                newRawmat.jobOrder = oldJO
                newRawmat.qty = item['qty']
                newRawmat.merchInventory.warehouseitems.all()[0].addQty(-(item['qty'])) 
                newRawmat.merchInventory.warehouseitems.all()[0].save2()
                newRawmat.purchasingPrice = item['purchasingPrice']
                newRawmat.totalCost = item['totalCost']
                newRawmat.save()
                request.user.branch.rawMaterials.add(newRawmat)
                # JE THEN DELETE

        for item in oldJO.rawmaterials.exclude(pk__in=newRawMatIDS):
            # JE HERE #

            # JE END  #
            item.delete()



        labor = Decimal (0)
        # for item in request.data['directlabor']:
            # dl = DirectLabor()
            # try:
            #     dl.expenses = AccountChild.objects.get(pk=item['expenses'])
            # except Exception as e:
            #     print(e)
            #     dl.expenses = None
            # dl.cost = item['cost']
            # dl.jobOrder = jo
            # dl.save()
            # request.user.branch.directLabor.add(dl)
            # labor += dl.cost
        for item in newJO['directlabor']:
            if oldJO.directlabor.filter(pk=item['id']):
                diff = Decimal(0)
                oldDirectLabor = oldJO.directlabor.filter(pk=item['id'])[0]
                if oldDirectLabor.cost > Decimal(item['cost']):
                    diff += abs(oldDirectLabor.cost - Decimal(item['cost']))
                    oldDirectLabor.cost -= diff
                    oldDirectLabor.save()

                elif oldDirectLabor.cost < Decimal(item['cost']):
                    diff += (abs(oldDirectLabor.cost - Decimal(item['cost'])))
                    oldDirectLabor.cost += diff
                    oldDirectLabor.save()

        overhead = Decimal(0)
        # for item in request.data['overheadexpenses']:
        #     if item['expenses']:
        #         ov = OverheadExpenses()
        #         ov.expenses = AccountChild.objects.get(pk=item['expenses'])
        #         ov.cost = item['cost']
        #         ov.jobOrder = jo
        #         ov.save()
        #         request.user.branch.overheadExpenses.add(ov)
        #         overhead += ov.cost
        
        newOverheadIDS = []
        for item in newJO['overheadexpenses']:
            if oldJO.overheadexpenses.filter(pk=item['id']):
                oldOverhead = oldJO.overheadexpenses.filter(pk=item['id'])[0]
                diff = Decimal(0)
                if oldOverhead.cost > Decimal(item['cost']):
                    diff += abs(oldOverhead.cost - Decimal(item['cost']))
                    oldOverhead.cost -= diff
                    oldOverhead.save()

                elif oldOverhead.cost < Decimal(item['cost']):
                    diff += abs(oldOverhead.cost + Decimal(item['cost']))
                    oldOverhead.cost += diff
                    oldOverhead.save()

            else:
                newOverheadIDS.append(item['id'])
                newOverhead = OverheadExpenses()
                try:
                    newOverhead.expenses = AccountChild.objects.get(pk=item['expenses'])
                except Exception as e:
                    print(e)
                    newOverhead.expenses = None
                newOverhead.cost = Decimal(item['cost'])
                newOverhead.jobOrder = oldJO
                newOverhead.save()
                request.user.branch.overheadExpenses.add(newOverhead)

                # JE BELOW #


        for item in oldJO.overheadexpenses.exclude(pk__in=newOverheadIDS):
            # JE BELOW #

            # WHAT IS LEFT FROM THE EXCLUDE MUST BE DELETED
            item.delete()



        # for item in request.data['finalproduct']:
        #     if item['name']:
        #         finalProduct = FinalProduct()
        #         finalProduct.name = item['name']
        #         finalProduct.qty = item['qty']
        #         finalProduct.unitCost = item['unitCost']
        #         finalProduct.totalCost = item['totalCost']
        #         finalProduct.jobOrder = jo
        #         finalProduct.save()
        #         request.user.branch.finalProduct.add(finalProduct)

        for item in newJO['finalproduct']:
            if oldJO.finalproduct.filter(pk=item['id']):
                diff = Decimal(0)
                oldFinalProduct = oldJO.finalproduct.filter(pk=item['id'])[0]
                if oldFinalProduct.qty > Decimal(item['qty']):
                    diff += abs(oldFinalProduct.totalCost - Decimal(item['totalCost']))
                    oldFinalProduct.cost -= diff
                    oldFinalProduct.save()

                elif oldFinalProduct.qty < Decimal(item['qty']):
                    diff += abs(oldFinalProduct.totalCost - Decimal(item['totalCost']))
                    oldFinalProduct.cost += diff
                    oldFinalProduct.save()


        # for item in request.data['materiallosses']:
        #     if item['name']:
        #         losses = MaterialLosses()
        #         losses.name = item['name']
        #         losses.qty = item['qty']
        #         losses.unitCost = item['unitCost']
        #         losses.totalCost = item['totalCost']
        #         losses.jobOrder = jo
        #         losses.save()
        #         request.user.branch.materialLosses.add(losses)

        newMatLossesIDS = []
        for item in newJO['materiallosses']:
            if oldJO.materiallosses.filter(pk=item['id']):
                oldMatLosses = oldJO.materiallosses.filter(pk=item['id'])[0]
                diff = Decimal(0)
                if oldMatLosses.qty < Decimal(item['qty']):
                    diff = abs(oldMatLosses.qty - Decimal(item['qty']))
                    oldMatLosses.qty += diff
                    oldMatLosses.unitCost = item['unitCost']
                    oldMatLosses.totalCost = item['totalCost']
                    oldMatLosses.save()

                elif oldMatLosses.qty > Decimal(item['qty']):
                    diff = abs(oldMatLosses.qty - Decimal(item['qty']))
                    oldMatLosses.qty -= diff
                    oldMatLosses.unitCost = item['unitCost']
                    oldMatLosses.totalCost = item['totalCost']
                    oldMatLosses.save()

            else:
                newMatLossesIDS.append(item['id'])
                newMatLosses = MaterialLosses()
                newMatLosses.name = item['name']
                newMatLosses.qty = item['qty']
                newMatLosses.unitCost = item['unitCost']
                newMatLosses.totalCost = item['totalCost']
                newMatLosses.jobOrder = oldJO
                newMatLosses.save()
                request.user.branch.materialLosses.add(newMatLosses)

        for item in oldJO.materiallosses.exclude(pk__in=newMatLossesIDS):
            # JE HERE #

            # JE END  #
            item.delete()
        
        if not rawmat == Decimal(0):
            jeAPI(request, j, 'Credit', dChildAccount.inventory, rawmat)
        if not overhead == Decimal(0):
            jeAPI(request, j, 'Credit', dChildAccount.factorySupplies, overhead)
        if not labor == Decimal(0):
            jeAPI(request, j, 'Credit', dChildAccount.laborExpense, labor)

        jeAPI(request, j, 'Debit', dChildAccount.workInProgress, rawmat+overhead+labor)
        
        oldJO.jobOrderCost = request.data['jobOrderCost']
        oldJO.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class JobOrderFinish(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        jo = JobOrder.objects.get(pk=request.data['id'])
        jo.datatimeFinished = datetime.datetime.now()
        jo.status = 'finished'
        jo.save()

        j = Journal()

        j.code = jo.code
        j.datetimeCreated = jo.datetimeCreated
        j.createdBy = jo.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)
        
        addloss = Decimal(0)
        for loss in jo.materiallosses.all():
            addloss += loss.totalCost

        if jo.method == 'Absorption':
            jeAPI(request, j, 'Credit', dChildAccount.workInProgress, jo.jobOrderCost)
            jeAPI(request, j, 'Credit', dChildAccount.materialLosses, addloss)
            jeAPI(request, j, 'Debit', dChildAccount.manuInventory, (jo.jobOrderCost + addloss))
        elif jo.method == 'Direct':
            jeAPI(request, j, 'Credit', dChildAccount.workInProgress, jo.jobOrderCost)
            jeAPI(request, j, 'Debit', dChildAccount.manuInventory, jo.jobOrderCost)
            jeAPI(request, j, 'Credit', dChildAccount.materialLosses, addloss)
            jeAPI(request, j, 'Debit', dChildAccount.cashOnHand, addloss)

        # exp= Decimal(0)
        # for expense in jo.overheadexpenses.all():
        #     jeAPI(request, j, 'Credit', expense.expenses, expense.cost)
        #     exp += expense.cost
        # jeAPI(request, j, 'Debit', dChildAccount.factorySupplies, exp)



        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

        