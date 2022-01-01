from rest_framework.views import APIView
from ..models import *
from django.http.response import FileResponse, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
import datetime
from .journalAPI import jeAPI
import io
import xlsxwriter
import string

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

        # salariesExpense = Decimal(0)
        # salariesPayable = Decimal(0)
        # bonus = Decimal(0)
        # monthPay13 = Decimal(0)
        # deminimis = Decimal(0)
        # hdmfER = Decimal(0)
        # phicER = Decimal(0)
        # sssER = Decimal(0)
        # sssPayable = Decimal(0)
        # phicPayable = Decimal(0)
        # hdmfPayable = Decimal(0)
        # withholdingTax = Decimal(0)
        # dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        

        for user in users:
            holidays = Holiday.objects.filter(date__range=[dateStart, dateEnd], type='rh')
            holidays = list(holidays)
            deminimis = Decimal(0)
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

            # INIT FOR BASIC PAY #
            bp = Decimal(0)

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

                    bp += dtr.bh * rates.bh * Decimal(user.rate/8)

                    if dtr.rh or dtr.sh or dtr.shw or dtr.rd or dtr.rhrd or dtr.shrd:
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
                    else:
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

            payroll.basicPay = bp

            payroll.grossPayBeforeBonus = \
            payroll.bh + \
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
            # salariesExpense += payroll.grossPayBeforeBonus
            payroll.grossPayAfterBonus = payroll.grossPayBeforeBonus

            #### 13 MONTH PAY ####
            usersW13thAlready = []
            if payroll.dateEnd == "{}-12-25".format(year):
                # INIT USERBASICPAY
                userBasicPay = Decimal(0)
    
                # LOOP ALL PAYROLL OF USER FOR THE WHOLE YEAR
                for pyroll in user.payroll.filter(year=year):
                    userBasicPay += pyroll.basicPay
    
                # CALCULATIONS OF 13TH MONTH PAY
                month13thPay = Decimal(userBasicPay/Decimal(12))
                
                m13p = Bonus13th()
                m13p.user = user
                m13p.year = year
                m13p.amount = month13thPay
                m13p.save()
                request.user.branch.bonus13th.add(m13p)

                bns = BonusPay()
                bns.user = user
                bns.payroll = payroll
                bns.name = '13th Month Pay'
                bns.amount = m13p.amount
                bns.save()
                request.user.branch.bonusPay.add(bns)

            try:
                allPayrollThisYear = user.payroll.filter(year=dateEnd.split('-')[0])
            except Exception as e:
                print(e)
                allPayrollThisYear = []

            print('all payroll', allPayrollThisYear)
            
            totalBonus = Decimal(0)
            totalBonusThisPeriod = Decimal(0)
            taxedbonus = Decimal(0)

            for bonuspay in user.bonuspay.all():
                if not bonuspay.payroll:
                    bonuspay.payroll = payroll
                    bonuspay.save()

            for bonuses in payroll.bonuspay.all():
                payroll.grossPayAfterBonus += bonuses.amount
                totalBonusThisPeriod += bonuses.amount
            
            # bonus += totalBonusThisPeriod
            # print('bonus ', bonus)

            for pay in allPayrollThisYear:
                for b in pay.bonuspay.all():
                    totalBonus += b.amount
                    
            print(totalBonus, 'TotalBonus')
            if (totalBonus) > Decimal(90000):
                print('bonus1')
                if totalBonus - (totalBonusThisPeriod) < Decimal(90000):
                    payroll.netPayBeforeTaxes = (payroll.grossPayBeforeBonus + (totalBonus - Decimal(90000)))
                    payroll.netPayAfterTaxes += totalBonusThisPeriod - (totalBonus - Decimal(90000))
                    print(payroll.netPayBeforeTaxes)
                else:
                    payroll.netPayBeforeTaxes = payroll.grossPayAfterBonus
                    print(payroll.netPayBeforeTaxes)
                taxedbonus = (totalBonus + totalBonusThisPeriod - Decimal(90000))
            else:
                print('bonus2')
                payroll.netPayBeforeTaxes = payroll.grossPayBeforeBonus

            # SCENARIOS
            # totalBonus = 92k
            # currentBonus = 4k
            # previousTotalBonus = 88k
            
            # if 92k - 4k < 90k
            # if 96 - 4k < 90k

            # totalBonus = 93k
            # currentBonus = 5k
            # previousBonus = 88k

            # netpayBeforeTax = 93k - (totalBonus - 90k)
            # netpayBeforeTax = grosspayBeforeTax + (totalBonus - 90k)
            # netpayaftertax += (currentbonus - (totalbonus -90k))
                
            #### END ####

            taxableBenefit = 0
            untaxableBenefit = 0
            
            for benefitOfUser in user.deminimisofuser.all():
                if benefitOfUser.amount > DeMinimis.objects.get(name__iexact=benefitOfUser.name).limit:
                    taxedBenefit = DeMinimisPay()
                    taxedBenefit.user = request.user
                    taxedBenefit.payroll = payroll
                    taxedBenefit.name = "Taxable " + benefitOfUser.name
                    taxedBenefit.amount = benefitOfUser.amount - DeMinimis.objects.get(name__iexact=benefitOfUser.name).limit
                    taxedBenefit.taxable = True
                    taxedBenefit.save()
                    request.user.branch.deMinimisPay.add(taxedBenefit)
                    payroll.grossPayAfterBonus += taxedBenefit.amount
                    taxableBenefit += taxedBenefit.amount

                    benefitPay = DeMinimisPay()
                    benefitPay.user = request.user
                    benefitPay.payroll = payroll
                    benefitPay.name = benefitOfUser.name
                    benefitPay.amount = DeMinimis.objects.get(name__iexact=benefitOfUser.name).limit
                    benefitPay.taxable = False
                    benefitPay.save()
                    request.user.branch.deMinimisPay.add(benefitPay)
                    payroll.grossPayAfterBonus += benefitPay.amount
                    untaxableBenefit += benefitPay.amount

                else:
                    benefitPay = DeMinimisPay()
                    benefitPay.user = request.user
                    benefitPay.payroll = payroll
                    benefitPay.name = benefitOfUser.name
                    benefitPay.amount = benefitOfUser.amount
                    benefitPay.taxable = False
                    benefitPay.save()
                    request.user.branch.deMinimisPay.add(benefitPay)
                    payroll.grossPayAfterBonus += benefitPay.amount
                    untaxableBenefit += benefitPay.amount

                deminimis += benefitOfUser.amount

            #### INITIALIZE MONTHY PAYS #####
            monthlyBasicPay = previousPayroll.basicPay + payroll.basicPay
            monthlyGrossPayBeforeBonus = previousPayroll.grossPayBeforeBonus + payroll.grossPayBeforeBonus
            
            
            ##### TO CHECK IF PAYROLL IS FOR SECOND PERIOD #####
            dateObj = datetime.datetime.strptime(payroll.dateEnd, '%Y-%m-%d')
            employeeLoan = 0
            if dateObj.day == 10:
                ##### LOAD DEDUCTIONS #####
                firstPeriod = [
                    1,2,3,4,5,6,7,8,9,10,26,27,28,29,30,31
                ]
                for loan in user.loans.all():
                    if not loan.fullyPaid and loan.startOfAmortization <= datetime.date(int(dateEnd.split("-")[0]), int(dateEnd.split("-")[1]), int(dateEnd.split("-")[2])) and loan.startOfAmortization.day in firstPeriod:
                        print('bigb0ss')
                        userLoan = LoanDeduction()
                        userLoan.user = user
                        userLoan.payroll = payroll
                        userLoan.amount = loan.monthlyAmortization
                        userLoan.loan = loan
                        userLoan.loanFrom = loan.loanFrom
                        loan.amountPaid += userLoan.amount
                        if loan.amountPaid >= loan.totalWithInterest:
                            loan.fullyPaid = True
                        loan.save()
                        userLoan.save()
                        request.user.branch.loanDeduction.add(userLoan)
                        employeeLoan += userLoan.amount
                        
                
            if dateObj.day == 25:
                ##### LOAN DEDUCTION #####
                secondPeriod = [
                    11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
                ]
                for loan in user.loans.all():
                    if not loan.fullyPaid and loan.startOfAmortization <= datetime.date(int(dateEnd.split("-")[0]), int(dateEnd.split("-")[1]), int(dateEnd.split("-")[2])) and loan.startOfAmortization.day in secondPeriod:
                        print('bigb0ss')
                        userLoan = LoanDeduction()
                        userLoan.user = user
                        userLoan.payroll = payroll
                        userLoan.amount = loan.monthlyAmortization
                        userLoan.loan = loan
                        userLoan.loanFrom = loan.loanFrom
                        loan.amountPaid += userLoan.amount
                        if loan.amountPaid >= loan.totalWithInterest:
                            loan.fullyPaid = True
                        loan.save()
                        userLoan.save()
                        request.user.branch.loanDeduction.add(userLoan)
                        employeeLoan += userLoan.amount

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
                        # sssER += sssDeduction.er
                        # sssPayable += (sssDeduction.er + sssDeduction.ee)

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
                        # phicER += phicDeduction.er
                        # phicPayable += (phicDeduction.er + phicDeduction.ee)
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
                        # phicER += phicDeduction.er
                        # phicPayable += (phicDeduction.er + phicDeduction.ee)
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
                        # phicER += phicDeduction.er
                        # phicPayable += (phicDeduction.er + phicDeduction.ee)

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
                # hdmfER += pagibigDeduction.amount
                # hdmfPayable += (pagibigDeduction.amount*2)
                
            monthlyGrossPayAfterBonus = previousPayroll.grossPayAfterBonus + payroll.grossPayAfterBonus
            monthlyNetPayBeforeTaxes = previousPayroll.netPayBeforeTaxes + payroll.netPayBeforeTaxes
            montlyNetPayAfterTaxes = previousPayroll.netPayAfterTaxes = payroll.netPayAfterTaxes

            ##### TAX #####
            incomeTaxTable = IncomeTaxTable.objects.all()

            taxDeductedObj = EmployeeTaxDeduction()

            payroll.netPayBeforeTaxes += taxableBenefit

            print('taxableBenefit', taxableBenefit)

            taxDeducted = 0
            for tax in incomeTaxTable:
                if tax.lowerLimit < (payroll.netPayBeforeTaxes) <= tax.upperLimit:
                    print(taxedbonus)
                    taxDeducted = ((((payroll.netPayBeforeTaxes) - tax.lowerLimit)) * tax.percentDeduction) + tax.fixedDeduction

                    taxDeductedObj.user = user
                    taxDeductedObj.payroll = payroll
                    taxDeductedObj.amount = taxDeducted
                    taxDeductedObj.incometaxtable = tax
                    taxDeductedObj.save()

                    

                    # withholdingTax += taxDeducted

            print(payroll.netPayBeforeTaxes, 'netpaybeforetaxes')
            payroll.netPayAfterTaxes += payroll.netPayBeforeTaxes - taxDeducted
 
            payroll.netPayAfterTaxes += untaxableBenefit
            payroll.netPayAfterTaxes -= employeeLoan
            if totalBonus < Decimal(90000):
                payroll.netPayAfterTaxes += payroll.grossPayAfterBonus - payroll.grossPayBeforeBonus - deminimis
            # salariesPayable += payroll.netPayAfterTaxes
               
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

class GenerateAnnualizationView(APIView):
    def get(self, request):
        print(request.GET['year'])
        if Annualization.objects.filter(year = request.GET['year']):
            return redirect('/ems-payroll/')
            
        annual = Annualization()
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()

        #### ENTER FOR LOOP BELOW ####
        # worksheet.write(row, col, data)
        HEADERS = [
            'Employees',
            'Class',
            '13th Month Pay and other Bonuses',
            'Total Basic Pay',
            'Total Holiday Pay',
            'Total OT Pay',
            'Total ND Pay',
            'Total NDOT Pay',
            'Total Hazard Pay',
            'Total De Minimis Pay',
            'Total SSS PHIC HDMF',
            'Total Gross Pay',
            'Total Non-Taxable',
            'Total Withholding'
        ]

        row = 0
        col = 0

        for header in HEADERS:
            worksheet.write(row, col, header)
            worksheet.set_column(row, col, 20)
            col += 1

        employees = request.user.branch.user.all().exclude(authLevel='dtr')

        for employee in employees:
            row += 1
            col = 0

            bonus13th = Decimal(0)
            data = {
                'name': '',
                'class': '',
                'bonusand13th': Decimal(0),
                'basic': Decimal(0),
                'holiday': Decimal(0),
                'ot': Decimal(0),
                'nd': Decimal(0),
                'ndot': Decimal(0),
                'hazard': Decimal(0),
                'deminimis': Decimal(0),
                'deductions': Decimal(0),
                'gross': Decimal(0),
                'nontax': Decimal(0),
                'withhold': Decimal(0)
            }

            data['name'] = employee.first_name + " " + employee.last_name

            for payroll in employee.payroll.filter(year=request.GET['year']):
                data['basic'] += payroll.basicPay
                data['holiday'] += payroll.holidayPay + payroll.rh + payroll.sh + payroll.shw
                data['ot'] += payroll.ot + payroll.rdot + payroll.rhot + payroll.shot + payroll.shwot + payroll.rhrdot + payroll.shrdot
                data['nd'] += payroll.nd + payroll.rdnd + payroll.rhnd + payroll.shnd + payroll.shwnd + payroll.rhrdnd + payroll.shrdnd
                data['ndot'] += payroll.ndot + payroll.rdndot + payroll.rhndot + payroll.shndot + payroll.shwndot + payroll.rhrdndot + payroll.shrdndot
                data['gross'] += payroll.grossPayAfterBonus
                
                try:
                    for bonus in payroll.bonuspay.all():
                        data['bonusand13th'] += bonus.amount
                except Exception as e:
                    print(e)

                try:
                    for deminimis in payroll.deminimispay.all():
                        data['deminimis'] += deminimis.amount
                except Exception as e:
                    print(e)

                try:
                    data['deductions'] += payroll.sssemployeededuction.ee
                except Exception as e:
                    print(e)

                try:
                    data['deductions'] += payroll.phicemployeededuction.ee
                except Exception as e:
                    print(e)
                
                try:
                    data['deductions'] += payroll.pagibigemployeededuction.amount
                except Exception as e:
                    print(e)

                try:
                    data['withhold'] += payroll.employeetaxdeduction.amount
                except Exception as e:
                    print(e)

                try:
                    for bonus13 in employee.bonus13th.all():
                        data['bonusand13th'] += bonus13.amount
                except Exception as e:
                    print(e)

            for key, val in data.items():
                worksheet.write(row, col, val)
                col += 1
            

        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Annualization.xlsx')

class PayrollAddBonus(APIView):
    def post(self, request):

        for data in request.data:
            employee = User.objects.get(id = data['user']['id'])
            for bonus in data['user']['bonus']:
                if not bonus['name'] or not bonus['amount']:
                    continue
                bonusPay = BonusPay()
                bonusPay.user = employee
                bonusPay.name = bonus['name']
                bonusPay.amount = bonus['amount']
                bonusPay.save()
                request.user.branch.bonusPay.add(bonusPay)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
            

class Give13thMonthPay(APIView):
    def post(self, request):
        """ THIS CODE IS GENERATE 13TH MONTH PAY 
        STARTING FROM DEC 26 OF THE PREVIOUS YEAR 
        TO CURRENT YEAR """

        year = request.data['year']

        users = request.user.branch.user.filter(payrollable = True)

        usersW13thAlready = []

        # LOOP ALL USERS OF THAT BRANCH
        for user in users:
            # INIT USERBASICPAY
            userBasicPay = Decimal(0)

            # LOOP ALL PAYROLL OF USER FOR THE WHOLE YEAR
            for payroll in user.payroll.filter(year=year):
                userBasicPay += payroll.basicPay

            # CALCULATIONS OF 13TH MONTH PAY
            if user.bonus13th.filter(year=year):
                usersW13thAlready.append("{} {}".format(user.first_name, user.last_name))
                continue
            month13thPay = Decimal(userBasicPay/Decimal(12))
            
            m13p = Bonus13th()
            m13p.user = user
            m13p.year = year
            m13p.amount = month13thPay
            m13p.save()
            request.user.branch.bonus13th.add(m13p)
        
        if usersW13thAlready == []:
            sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        else: 
            sweetify.sweetalert(request, icon='success', title='Success!', text="Employees with 13th month pay already: \n\n {}".format(usersW13thAlready), persistent='Dismiss')
        return JsonResponse(0, safe=False)

class Give13thMonthPayIndividual(APIView):
    def post(self, request):
        data = request.data
        user = request.user.branch.user.get(pk=data['user'])
        if user.bonus13th.filter(year=data['year']):
            sweetify.sweetalert(request, icon='warning', title="", html='<b>User already has 13th month pay!</b>', persistent='Dismiss')
            return JsonResponse(0, safe=False)

        if data['year'] == '':
            sweetify.sweetalert(request, icon='warning', title="",  html='<b>No Year Selected</b>', persistent='Dismiss')
            return JsonResponse(0, safe=False)
        

        userBasicPay = Decimal(0)

        # LOOP ALL PAYROLL OF USER FOR THE WHOLE YEAR
        for payroll in user.payroll.filter(year=data['year']):
            userBasicPay += payroll.basicPay

        month13thPay = Decimal(userBasicPay/Decimal(12))
            
        m13p = Bonus13th()
        m13p.user = user
        m13p.year = data['year']
        m13p.amount = month13thPay
        m13p.save()
        request.user.branch.bonus13th.add(m13p)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)