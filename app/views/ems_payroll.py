from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
import datetime

class EMS_PayrollView(View):
    def get(self, request):
        try: 
            y = request.GET['year']
            dateRange = request.GET['dateRange']
            dateStart = dateRange.split(' ')[0]
            dateEnd = dateRange.split(' ')[1]
            context = {
                'payrolls': request.user.branch.payroll.filter(year=y, dateStart=dateStart, dateEnd=dateEnd)
            }
        except Exception as e:
            print(e)
            context = {
                'payrolls': None
            }
        return render(request, 'ems-payroll.html', context)

class EMS_EditPayrollView(View):
    def get(self, request):
        return render(request, 'ems-edit-payroll.html')

class EMS_GeneratePayroll(APIView):
    def post(self, request):
        users = User.objects.filter(branch = request.user.branch, payrollable = True)
        year = request.data[0]
        period = request.data[1]
        dateRange = request.data[2]

        dateStart = dateRange.split(' ')[0]
        dateEnd = dateRange.split(' ')[1]

        

        for user in users:
            holidays = Holiday.objects.filter(date__range=[dateStart, dateEnd], type='rh')
            holidays = list(holidays)
            print(dateStart)
            x = dateStart.split('-')
            x[2] = str(int(x[2]) - 1)
            previousDateEnd = "-".join(x)
            print(previousDateEnd)
            try:
                previousPayroll = user.payroll.get(dateEnd=previousDateEnd)
            except Exception as e:
                print(e)
                previousPayroll = Payroll()
                previousPayroll.basicPay = Decimal(0)
                previousPayroll.grossPayBeforeBonus = Decimal(0)
                previousPayroll.grossPayAfterBonus = Decimal(0)
                previousPayroll.netPayAfterTaxes = Decimal(0)
                previousPayroll.netPayBeforeTaxes = Decimal(0)
            try:
                if user.payroll.filter(dateStart=dateStart, dateEnd=dateEnd):
                    continue
            except:
                pass
            payroll = Payroll()
            payroll.year = year
            payroll.dateStart = dateStart
            payroll.dateEnd = dateEnd
            payroll.dateGenerated = datetime.date.today()
            payroll.user = user
            if previousPayroll.dateGenerated:
                payroll.previousPayroll = previousPayroll
            payroll.save()
            request.user.branch.payroll.add(payroll)
            rates = request.user.branch.ratesGroup.get(name='DOLE Standard')

            for dtr in user.dtr.filter(date__range=[dateStart, dateEnd]):
                if not dtr.payroll:
                    dtr.payroll = payroll
                    dtr.save()
                    print(holidays)
                    for dtrHoliday in list(dtr.dtrdaycategory.all()):
                        print(dtrHoliday.holiday)
                        try:
                            holidays.remove(dtrHoliday.holiday)
                        except:
                            pass

                    payroll.bh += dtr.bh * rates.bh * Decimal(user.rate/8)
                    payroll.ot += dtr.ot * rates.ot * Decimal(user.rate/8)
                    payroll.ut += dtr.ut * rates.ut * Decimal(user.rate/8)
                    payroll.nd += dtr.nd * rates.nd * Decimal(user.rate/8)
                    payroll.ndot += dtr.ndot * rates.ndot * Decimal(user.rate/8)
                    payroll.rd += dtr.rd * rates.rd * Decimal(user.rate/8)
                    payroll.rdot += dtr.rdot * rates.rdot * Decimal(user.rate/8)
                    payroll.rdnd += dtr.rdnd * rates.rdnd * Decimal(user.rate/8)
                    payroll.rdndot += dtr.rdndot * rates.rdndot * Decimal(user.rate/8)
                    payroll.rh += dtr.rh * rates.rh * Decimal(user.rate/8)
                    payroll.rhot += dtr.rhot * rates.rhot * Decimal(user.rate/8)
                    payroll.rhnd += dtr.rhnd * rates.rhnd * Decimal(user.rate/8)
                    payroll.rhndot += dtr.rhndot * rates.rhndot * Decimal(user.rate/8)
                    payroll.sh += dtr.sh * rates.sh * Decimal(user.rate/8)
                    payroll.shot += dtr.shot * rates.shot * Decimal(user.rate/8)
                    payroll.shnd += dtr.shnd * rates.shnd * Decimal(user.rate/8)
                    payroll.shndot += dtr.shndot * rates.shndot * Decimal(user.rate/8)
                    payroll.shw += dtr.shw * rates.shw * Decimal(user.rate/8)
                    payroll.shwot += dtr.shwot * rates.shwot * Decimal(user.rate/8)
                    payroll.shwnd += dtr.shwnd * rates.shwnd * Decimal(user.rate/8)
                    payroll.shwndot += dtr.shwndot * rates.shwndot * Decimal(user.rate/8)
                    payroll.rhrd += dtr.rhrd * rates.rhrd * Decimal(user.rate/8)
                    payroll.rhrdot += dtr.rhrdot * rates.rhrdot * Decimal(user.rate/8)
                    payroll.rhrdnd += dtr.rhrdnd * rates.rhrdnd * Decimal(user.rate/8)
                    payroll.rhrdndot += dtr.rhrdndot * rates.rhrdndot * Decimal(user.rate/8)
                    payroll.shrd += dtr.shrd * rates.shrd * Decimal(user.rate/8)
                    payroll.shrdot += dtr.shrdot * rates.shrdot * Decimal(user.rate/8)
                    payroll.shrdnd += dtr.shrdnd * rates.shrdnd * Decimal(user.rate/8)
                    payroll.shrdndot += dtr.shrdndot * rates.shrdndot * Decimal(user.rate/8)

                    payroll.bhTotalHours += dtr.bh
                    payroll.otTotalHours += dtr.ot
                    payroll.utTotalHours += dtr.ut
                    payroll.ndTotalHours += dtr.nd
                    payroll.ndotTotalHours += dtr.ndot
                    payroll.rdTotalHours += dtr.rd
                    payroll.rdotTotalHours += dtr.rdot
                    payroll.rdndTotalHours += dtr.rdnd
                    payroll.rdndotTotalHours += dtr.rdndot
                    payroll.rhTotalHours += dtr.rh
                    payroll.rhotTotalHours += dtr.rhot
                    payroll.rhndTotalHours += dtr.rhnd
                    payroll.rhndotTotalHours += dtr.rhndot
                    payroll.shTotalHours += dtr.sh
                    payroll.shotTotalHours += dtr.shot
                    payroll.shndTotalHours += dtr.shnd
                    payroll.shndotTotalHours += dtr.shndot
                    payroll.shwTotalHours += dtr.shw
                    payroll.shwotTotalHours += dtr.shwot
                    payroll.shwndTotalHours += dtr.shwnd
                    payroll.shwndotTotalHours += dtr.shwndot
                    payroll.rhrdTotalHours += dtr.rhrd
                    payroll.rhrdotTotalHours += dtr.rhrdot
                    payroll.rhrdndTotalHours += dtr.rhrdnd
                    payroll.rhrdndotTotalHours += dtr.rhrdndot
                    payroll.shrdTotalHours += dtr.shrd
                    payroll.shrdotTotalHours += dtr.shrdot
                    payroll.shrdndTotalHours += dtr.shrdnd
                    payroll.shrdndotTotalHours += dtr.shrdndot
                

            payroll.holidayPay = (len(holidays)*user.rate)

            payroll.basicPay = payroll.bh
            payroll.grossPayBeforeBonus = \
                payroll.basicPay + \
                payroll.ot + \
                payroll.ut + \
                payroll.nd + \
                payroll.ndot + \
                payroll.rd + \
                payroll.rdot + \
                payroll.rdnd + \
                payroll.rdndot + \
                payroll.rh + \
                payroll.rhot + \
                payroll.rhnd + \
                payroll.rhndot + \
                payroll.sh + \
                payroll.shot + \
                payroll.shnd + \
                payroll.shndot + \
                payroll.shw + \
                payroll.shwot + \
                payroll.shwnd + \
                payroll.shwndot + \
                payroll.rhrd + \
                payroll.rhrdot + \
                payroll.rhrdnd + \
                payroll.rhrdndot + \
                payroll.shrd + \
                payroll.shrdot + \
                payroll.shrdnd + \
                payroll.shrdndot

            # payroll.save()


            #### SOME SPECIAL CODES ####
            payroll.grossPayBeforeBonus += payroll.holidayPay
            payroll.grossPayAfterBonus = payroll.grossPayBeforeBonus

            try: 
                allPayrollThisYear = user.payroll.filter(year=dateEnd.split('-')[2])
            except:
                allPayrollThisYear = []
            
            totalBonus = Decimal(0)
            totalBonusThisPeriod = Decimal(0)

            for bonuses in payroll.bonuspay.all():
                payroll.grossPayAfterBonus += bonuses.amount
                totalBonusThisPeriod += bonuses.amount

            for pay in allPayrollThisYear:
                for bonus in pay.bonuspay:
                    totalBonus += bonus.amount

            if totalBonus >= Decimal(90000):
                if totalBonus - totalBonusThisPeriod < Decimal(90000):
                    payroll.grossPayAfterBonus += Decimal(90000) - (totalBonus - totalBonusThisPeriod)
                else:
                    payroll.grossPayAfterBonus += totalBonusThisPeriod
                payroll.netPayBeforeTaxes = payroll.grossPayAfterBonus
            else:
                payroll.netPayBeforeTaxes = payroll.grossPayBeforeBonus
                
            #### END ####

            
            for benefitOfUser in user.deminimisofuser.all():
                if benefitOfUser.amount > DeMinimis.objects.get(name=benefitOfUser.name).limit:
                    taxedBenefit = DeMinimisPay()
                    taxedBenefit.user = request.user
                    taxedBenefit.payroll = payroll
                    taxedBenefit.name = "Excess " + benefitOfUser.name
                    taxedBenefit.amount = benefitOfUser.amount - DeMinimis.objects.get(name=benefitOfUser.name).limit
                    taxedBenefit.taxable = True
                    taxedBenefit.save()
                    request.user.branch.deMinimisPay.add(taxedBenefit)
                    payroll.grossPayAfterBonus += taxedBenefit.amount

                    benefitPay = DeMinimisPay()
                    benefitPay.user = request.user
                    benefitPay.payroll = payroll
                    benefitPay.name = benefitOfUser.name
                    benefitPay.amount = DeMinimis.objects.get(name=benefitOfUser.name).limit
                    benefitPay.taxable = False
                    benefitPay.save()
                    request.user.branch.deMinimisPay.add(benefitPay)

                else:
                    benefitPay = DeMinimisPay()
                    benefitPay.user = request.user
                    benefitPay.payroll = payroll
                    benefitPay.name = benefitOfUser.name
                    benefitPay.amount = benefitOfUser.amount
                    benefitPay.taxable = False
                    benefitPay.save()
                    request.user.branch.deMinimisPay.add(benefitPay)

            #### INITIALIZE MONTHY PAYS #####
            monthlyBasicPay = previousPayroll.basicPay + payroll.basicPay
            monthlyGrossPayBeforeBonus = previousPayroll.grossPayBeforeBonus + payroll.grossPayBeforeBonus
            
            
            ##### TO CHECK IF PAYROLL IS FOR SECOND PERIOD #####
            dateObj = datetime.datetime.strptime(payroll.dateEnd, '%Y-%m-%d')
            if dateObj.day == 25:

                ##### SSS #####
                sss = SSSContributionRate.objects.all()
                for rates in sss:
                    if rates.lowerLimit <= monthlyGrossPayBeforeBonus < rates.upperLimit:
                        sssDeduction = SSSEmployeeDeduction()
                        sssDeduction.ee = rates.ee
                        sssDeduction.er = rates.er
                        sssDeduction.sssContributionRate = rates
                        sssDeduction.user = user
                        sssDeduction.payroll = payroll
                        sssDeduction.save()
                        request.user.branch.sssEmployeeDeduction.add(sssDeduction)

                        payroll.netPayBeforeTaxes -= sssDeduction.ee

                ##### PHILHEALTH #####
                phic = PHICContributionRate.objects.all()
                for rates in phic:
                    if rates.lowerLimit <= monthlyBasicPay <= rates.upperLimit:
                        phicDeduction = PHICEmployeeDeduction()
                        phicDeduction.ee = ((rates.rate/2)*monthlyBasicPay)
                        phicDeduction.er = ((rates.rate/2)*monthlyBasicPay)
                        phicDeduction.phicContributionRate = rates
                        phicDeduction.user = user
                        phicDeduction.payroll = payroll
                        phicDeduction.save()
                        request.user.branch.phicEmployeeDeduction.add(phicDeduction)
                        payroll.netPayBeforeTaxes -= phicDeduction.ee
                    elif monthlyBasicPay > rates.upperLimit:
                        phicDeduction = PHICEmployeeDeduction()
                        phicDeduction.ee = (rates.rate/2)*rates.upperLimit
                        phicDeduction.er = (rates.rate/2)*rates.upperLimit
                        phicDeduction.phicContributionRate = rates
                        phicDeduction.user = user
                        phicDeduction.payroll = payroll
                        phicDeduction.save()
                        request.user.branch.phicEmployeeDeduction.add(phicDeduction)
                        payroll.netPayBeforeTaxes -= phicDeduction.ee
                    elif monthlyBasicPay < rates.lowerLimit:
                        phicDeduction = PHICEmployeeDeduction()
                        phicDeduction.ee = (rates.rate/2)*rates.lowerLimit
                        phicDeduction.er = (rates.rate/2)*rates.lowerLimit
                        phicDeduction.phicContributionRate = rates
                        phicDeduction.user = user
                        phicDeduction.payroll = payroll
                        phicDeduction.save()
                        request.user.branch.phicEmployeeDeduction.add(phicDeduction)
                        payroll.netPayBeforeTaxes -= phicDeduction.ee

                ##### PAGIBIG #####
                pagibig = PagibigContributionRate.objects.latest('pk')
                pagibigDeduction = PagibigEmployeeDeduction()
                pagibigDeduction.payroll = payroll
                pagibigDeduction.amount = pagibig.rate
                pagibigDeduction.pagibigContributionRate = pagibig
                pagibigDeduction.user = user
                payroll.netPayBeforeTaxes -= pagibigDeduction.amount
                pagibigDeduction.save()
                request.user.branch.pagibigEmployeeDeduction.add(pagibigDeduction)
                
            monthlyGrossPayAfterBonus = previousPayroll.grossPayAfterBonus + payroll.grossPayAfterBonus
            monthlyNetPayBeforeTaxes = previousPayroll.netPayBeforeTaxes + payroll.netPayBeforeTaxes
            montlyNetPayAfterTaxes = previousPayroll.netPayAfterTaxes = payroll.netPayAfterTaxes

            ##### TAX #####
            incomeTaxTable = IncomeTaxTable.objects.all()

            taxDeductedObj = EmployeeTaxDeduction()

            for tax in incomeTaxTable:
                taxDeducted = 0
                if tax.lowerLimit < (payroll.netPayBeforeTaxes) <= tax.upperLimit:
                    taxDeducted = ((((payroll.netPayBeforeTaxes) - tax.lowerLimit)) * tax.percentDeduction) + tax.fixedDeduction

                    taxDeductedObj.user = user
                    taxDeductedObj.payroll = payroll
                    taxDeductedObj.amount = taxDeducted
                    taxDeductedObj.incometaxtable = tax
                    taxDeductedObj.save()

                    payroll.netPayAfterTaxes = payroll.netPayBeforeTaxes - taxDeducted
                
            payroll.save()
        return JsonResponse(0, safe=False)

class EMS_EditPayrollSave(APIView):
    def put(self, request, pk, format = None):

        payroll = Payroll.objects.get(pk=pk)

        edit = request.data

        payroll.bh = edit['bh']
        payroll.ot = edit['ot']
        payroll.ut = edit['ut']
        payroll.nd = edit['nd']
        payroll.ndot = edit['ndot']
        payroll.rd = edit['rd']
        payroll.rdot = edit['rdot']
        payroll.rdnd = edit['rdnd']
        payroll.rdndot = edit['rdndot']
        payroll.rh = edit['rh']
        payroll.rhot = edit['rhot']
        payroll.rhnd = edit['rhnd']
        payroll.rhndot = edit['rhndot']
        payroll.sh = edit['sh']
        payroll.shot = edit['shot']
        payroll.shnd = edit['shnd']
        payroll.shndot = edit['shndot']
        payroll.shw = edit['shw']
        payroll.shwot = edit['shwot']
        payroll.shwnd = edit['shwnd']
        payroll.shwndot = edit['shwndot']
        payroll.rhrd = edit['rhrd']
        payroll.rhrdot = edit['rhrdot']
        payroll.rhrdnd = edit['rhrdnd']
        payroll.rhrdndot = edit['rhrdndot']
        payroll.shrd = edit['shrd']
        payroll.shrdot = edit['shrdot']
        payroll.shrdnd = edit['shrdnd']
        payroll.shrdndot = edit['shrdndot']
        payroll.bhTotalHours = edit['bhTotalHours']
        payroll.otTotalHours = edit['otTotalHours']
        payroll.utTotalHours = edit['utTotalHours']
        payroll.ndTotalHours = edit['ndTotalHours']
        payroll.ndotTotalHours = edit['ndotTotalHours']
        payroll.rdTotalHours = edit['rdTotalHours']
        payroll.rdotTotalHours = edit['rdotTotalHours']
        payroll.rdndTotalHours = edit['rdndTotalHours']
        payroll.rdndotTotalHours = edit['rdndotTotalHours']
        payroll.rhTotalHours = edit['rhTotalHours']
        payroll.rhotTotalHours = edit['rhotTotalHours']
        payroll.rhndTotalHours = edit['rhndTotalHours']
        payroll.rhndotTotalHours = edit['rhndotTotalHours']
        payroll.shTotalHours = edit['shTotalHours']
        payroll.shotTotalHours = edit['shotTotalHours']
        payroll.shndTotalHours = edit['shndTotalHours']
        payroll.shndotTotalHours = edit['shndotTotalHours']
        payroll.shwTotalHours = edit['shwTotalHours']
        payroll.shwotTotalHours = edit['shwotTotalHours']
        payroll.shwndTotalHours = edit['shwndTotalHours']
        payroll.shwndotTotalHours = edit['shwndotTotalHours']
        payroll.rhrdTotalHours = edit['rhrdTotalHours']
        payroll.rhrdotTotalHours = edit['rhrdotTotalHours']
        payroll.rhrdndTotalHours = edit['rhrdndTotalHours']
        payroll.rhrdndotTotalHours = edit['rhrdndotTotalHours']
        payroll.shrdTotalHours = edit['shrdTotalHours']
        payroll.shrdotTotalHours = edit['shrdotTotalHours']
        payroll.shrdndTotalHours = edit['shrdndTotalHours']
        payroll.shrdndotTotalHours = edit['shrdndotTotalHours']
        payroll.basicPay = edit['basicPay']
        payroll.holidayPay = edit['holidayPay']
        payroll.grossPayBeforeBonus = edit['grossPayBeforeBonus']
        payroll.grossPayAfterBonus = edit['grossPayAfterBonus']
        payroll.netPayBeforeTaxes = edit['netPayBeforeTaxes']
        payroll.netPayAfterTaxes = edit['netPayAfterTaxes']

        try:
            payroll.sssemployeededuction.ee = edit['sssemployeededuction']['ee']
            payroll.sssemployeededuction.er = edit['sssemployeededuction']['er']
        except Exception as e:
            print(e)

        try:
            payroll.phicemployeededuction.ee = edit['phicemployeededuction']['ee']
            payroll.phicemployeededuction.er = edit['phicemployeededuction']['er']
        except Exception as e:
            print(e)

        try:
            payroll.pagibigemployeededuction.amount = edit['pagibigemployeededuction']['amount']
        except Exception as e:
            print(e)

        try:
            payroll.employeetaxdeduction.amount = edit['employeetaxdeduction']['amount']
        except Exception as e:
            print(e)

        for bonus in edit['bonuspay']:
            if payroll.bonuspay.filter(name=bonus['name']).exists():
                payroll.bonuspay.amount = bonus['amount']
            else:
                bonusPay = BonusPay()
                bonusPay.user = request.user
                bonusPay.payroll = payroll
                bonusPay.name = bonus['name']
                bonusPay.amount = bonus['amount']
                bonusPay.save()
        
        for benefit in edit['deminimispay']:
            if payroll.deminimispay.filter(name=benefit['name']).exists():
                payroll.deminimispay.amount = benefit['amount']
            else:
                deminimisPay = DeMinimisPay()
                deminimisPay.user = request.user
                deminimisPay.payroll = payroll
                deminimisPay.name = benefit['name']
                deminimisPay.amount = benefit['amount']
                deminimisPay.taxable = benefit['taxable']
                deminimisPay.save()

        payroll.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)