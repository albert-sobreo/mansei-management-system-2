from rest_framework.views import APIView
import datetime
from django.http.response import JsonResponse
from django.views import View
from ..models import *
from django.shortcuts import redirect, render, HttpResponse
from ..serializers import *
from rest_framework.response import Response
from decimal import Decimal
from django.core import serializers
import datetime
from django.core.exceptions import PermissionDenied

class DTRList(View):
    def get(self, request, format=None):
        if request.user.authLevel != 'dtr':
            raise PermissionDenied()
        context = {
            'User': User.objects.all()
        }
        return render(request, 'ems-dtr-list.html', context)


class FetchUserDTR(APIView):
    def get(self, request, format=None):
        user = User.objects.get(pk=request.GET['id'])
        startDate = request.GET['startDate']
        endDate = request.GET['endDate']

        try:
            dtrList = user.dtr.all().filter(date__range=[startDate, endDate])
        except:
            return JsonResponse(1, safe=False)

        # THIS BITCH CONTAINS OTHER STUFFS
        serializedDtrList = serializers.serialize('python', dtrList)
        
        # FILTERS THE GOOD STUFFS
        actualData = [d['fields'] for d in serializedDtrList]
        
        return JsonResponse (actualData, safe=False)



class DTRView(View):
    def get(self, request, format=None):
        if request.user.authLevel != 'dtr':
            raise PermissionDenied()
        return render(request, 'ems-dtr.html')

# RETURN MESSAGES
# 0 - SUCCESS
# 1 - DID NOT TIMEOUT

class DTRProcess(APIView):
    def timeIn(self, userID, request):
        employee = User.objects.get(idUser=userID)
        
        holidays = Holiday.objects.filter(date=datetime.date.today())

        dtr = DTR()
        dtr.dateTimeIn = datetime.datetime.now()
        dtr.user = employee
        dtr.date = datetime.date.today()
        dtr.save()
        request.user.branch.dtr.add(dtr)

        dtrDayCategory = DTRDayCategory()
        for holiday in holidays:
            dtrDayCategory.dtr = dtr
            dtrDayCategory.holiday = holiday
            dtrDayCategory.save()
    
    # def timeOut(self, userID):
    #     employee = User.objects.get(idUser=userID)
    
    #     dtr = employee.dtr.all().latest('pk')
    #     dtr.dateTimeOut = datetime.datetime.now()
    #     dtr.save()

    #     bh = Decimal(0)
    #     ut = Decimal(0)
    #     ot = Decimal(0)
        

    #     tolerance = datetime.timedelta(minutes=5)

    #     breakStart = datetime.datetime.combine(datetime.date.today(), datetime.time(12))
    #     breakEnd = datetime.datetime.combine(datetime.date.today(), datetime.time(13))

    #     scheduleTimeIn = datetime.datetime.combine(datetime.date.today(), employee.schedule.timeIn)
    #     scheduleTimeOut = datetime.datetime.combine(datetime.date.today(), employee.schedule.timeOut)

    #     durationSchedule = scheduleTimeOut - scheduleTimeIn - datetime.timedelta(hours=1) #timedelta
    #     durationDTR = dtr.dateTimeOut - dtr.dateTimeIn #timedelta
    #     durationDiff = abs(durationSchedule - durationDTR)
        

    #     timeInDiff = abs(scheduleTimeIn - dtr.dateTimeIn) #timedelta
    #     timeOutDiff = abs(scheduleTimeOut - dtr.dateTimeOut) #timedelta

    #     durationDTR = durationDTR - datetime.timedelta(hours=1) if dtr.dateTimeOut >= breakEnd and dtr.dateTimeIn <= breakStart else durationDTR

    #     # EARLY OR ON TIME
    #     if dtr.dateTimeIn <= scheduleTimeIn or timeInDiff < tolerance:
    #         durationDTR = durationDTR - timeInDiff
    #         timeInDiff = datetime.timedelta(0)
        
    #     # TIME IN ON TIME AND TIME OUT ON TIME
    #     if timeInDiff < tolerance and timeOutDiff < tolerance:
    #         rh = Decimal(8.0)
        
    #     # IF TIME IN ON TIME
    #     print(timeInDiff, timeOutDiff, durationDTR, durationSchedule)
        
    #     # if timeInDiff == datetime.timedelta(0):
    #     print(1)
    #     # UNDERTIME TIME OUT
    #     if timeOutDiff > tolerance:
    #         if dtr.dateTimeOut < scheduleTimeOut:
    #             print(2)
    #             ut += Decimal(timeOutDiff.seconds/3600)
    #             print(ut)
    #     # OVERTIME TIME OUT
    #         else:
    #             ot += Decimal(timeOutDiff.seconds/3600)
    #     # if timeOutDiff > tolerance and durationDTR > durationSchedule:
    #     #     print(3)
    #     #     
    #     rh += Decimal(durationDTR.seconds/3600)
    #     # IF TIME IN LATE
    #     # else:
    #     #     print(4)
    #     #     # UNDERTIME TIME OUT
    #     #     if durationDTR < durationSchedule and durationDiff > 2*tolerance:
    #     #         print(5)
    #     #         ut += Decimal(durationDiff.seconds/3600)
    #     #     if durationDTR > durationSchedule and durationDiff > 2*tolerance:
    #     #         print(6)
    #     #         ot += Decimal(durationDiff.seconds/3600)
    #     #     if durationDiff < 2*tolerance:
    #     #         print(7)
    #     #         rh = Decimal(8.0)
    #     ut += Decimal(timeInDiff.seconds/3600)
    #     print(ut)
    #     rh = rh - ot
    #     print(rh)

    #     dtr.rh = rh
    #     dtr.ut = ut
    #     dtr.ot = ot
    #     dtr.save()

    def timeOut(self, userID):
        employee = User.objects.get(idUser=userID)
    
        dtr = employee.dtr.all().latest('pk')
        dtr.dateTimeOut = datetime.datetime.now()
        dtr.save()

        bh = Decimal(0)
        ut = Decimal(0)
        ot = Decimal(0)
        nd = Decimal(0)
        ndot = Decimal(0)
        rd = Decimal(0)
        rdot = Decimal(0)
        rdnd = Decimal(0)
        rdndot = Decimal(0)
        rh = Decimal(0)
        rhot = Decimal(0)
        rhnd = Decimal(0)
        rhndot = Decimal(0)
        sh = Decimal(0)
        shot = Decimal(0)
        shnd = Decimal(0)
        shndot = Decimal(0)
        shw = Decimal(0)
        shwot = Decimal(0)
        shwnd = Decimal(0)
        shwndot = Decimal(0)
        rhrd = Decimal(0)
        rhrdot = Decimal(0)
        rhrdnd = Decimal(0)
        rhrdndot = Decimal(0)
        shrd = Decimal(0)
        shrdot = Decimal(0)
        shrdnd = Decimal(0)
        shrdndot = Decimal(0)
        
        tolerance = {
            'default': datetime.timedelta(minutes=5),
            'afterTimeOut': datetime.timedelta(minutes=30)
        }

        breakStart = datetime.datetime.combine(dtr.dateTimeIn.date(), datetime.time(12))
        breakEnd = datetime.datetime.combine(dtr.dateTimeIn.date(), datetime.time(13))

        breakNightStart = datetime.datetime.combine(dtr.dateTimeIn.date(), datetime.time(22))
        breakNightEnd = datetime.datetime.combine(dtr.dateTimeIn.date(), datetime.time(23))

        scheduleTimeIn = datetime.datetime.combine(dtr.dateTimeIn.date(), employee.schedule.timeIn)
        scheduleTimeOut = datetime.datetime.combine(dtr.dateTimeOut.date(), employee.schedule.timeOut)

        # durationSchedule = scheduleTimeOut - scheduleTimeIn - datetime.timedelta(hours=1) #timedelta
        
        # durationDiff = abs(durationSchedule - durationDTR)
        

        timeInDiff = abs(scheduleTimeIn - dtr.dateTimeIn) #timedelta
        timeOutDiff = abs(scheduleTimeOut - dtr.dateTimeOut) #timedelta

        print(timeInDiff)
        print(timeOutDiff)

        # EARLY TIME IN OR ON TIME
        if dtr.dateTimeIn <= scheduleTimeIn or timeInDiff < tolerance['default']:
            timeInDiff = datetime.timedelta(0)

        arrival = {
            'onTime': timeInDiff < tolerance['default'],
            'offTime': timeInDiff > tolerance['default'],
        }

        departure = {
            "onTime": (timeOutDiff < tolerance['default'] and dtr.dateTimeOut < scheduleTimeOut) or (timeOutDiff < tolerance['afterTimeOut'] and dtr.dateTimeOut > scheduleTimeOut),
            'offTime': (timeOutDiff > tolerance['default'] and dtr.dateTimeOut < scheduleTimeOut) or (timeOutDiff > tolerance['afterTimeOut'] and dtr.dateTimeOut > scheduleTimeOut),
            'earlyDeparture': timeOutDiff > tolerance['default'] and dtr.dateTimeOut < scheduleTimeOut,
            'lateDeparture': timeOutDiff > tolerance['afterTimeOut'] and dtr.dateTimeOut > scheduleTimeOut
        }

        print(arrival)
        print(departure)

        # A FUNCTION TO DEDUCT BREAK FROM DURATION DTR
        def deductBreak(time):
            return time - datetime.timedelta(hours=1) if dtr.dateTimeOut >= breakEnd and dtr.dateTimeIn <= breakStart else time
        
        def deductBreakNight(time):
            return time - datetime.timedelta(hours=1) if dtr.dateTimeOut >= breakNightEnd and dtr.dateTimeIn <= breakNightStart else time

        def getND(mytimein, mytimeout):
            relevantTimeIn = None
            releventTimeOut = None
            relevantDIFF = datetime.timedelta(0)

            if datetime.datetime.combine(mytimein.date(), datetime.time(22)) <= mytimeout <= datetime.datetime.combine((mytimein.date() + datetime.timedelta(days=1)), datetime.time(6)) or \
                datetime.datetime.combine(mytimein.date(), datetime.time(22)) < datetime.datetime.combine((mytimein.date() + datetime.timedelta(days=1)), datetime.time(6)) <= mytimeout:
                print('1-0')
                if mytimein < datetime.datetime.combine(mytimein.date(), datetime.time(22)):
                    print('1-1')
                    releventTimeIn = datetime.datetime.combine(mytimein.date(), datetime.time(22))
                elif mytimein >= datetime.datetime.combine(mytimein.date(), datetime.time(22)):
                    print('1-2')
                    relevantTimeIn = mytimein

                if mytimeout <= datetime.datetime.combine((mytimein.date() + datetime.timedelta(days=1)), datetime.time(6)):
                    print('1-3')
                    releventTimeOut = mytimeout
                elif mytimeout > datetime.datetime.combine((mytimein.date() + datetime.timedelta(days=1)), datetime.time(6)):
                    print('1-4')
                    releventTimeOut = datetime.datetime.combine(mytimeout.date(), datetime.time(6))

                relevantDIFF = abs(releventTimeOut - releventTimeIn)
                if employee.schedule.timeIn >= datetime.time(18):
                    relevantDIFF = deductBreakNight(relevantDIFF)

            return Decimal(relevantDIFF.seconds/3600)

        def getOTMark(scheduleTimeIn):
            return scheduleTimeIn + datetime.timedelta(hours=9)

        def getNDOT(mytimein, mytimeout, scheduletimein, scheduletimeout):
            otMark = scheduletimein + datetime.timedelta(hours=9)

            relevantTimeIn = None
            releventTimeOut = None

            if datetime.datetime.combine(mytimein.date(), datetime.time(22)) <= mytimeout <= datetime.datetime.combine((mytimein.date() + datetime.timedelta(days=1)), datetime.time(6)):
                
                if otMark.time() >= datetime.time(22) or otMark.time() <= datetime.time(6):
                    
                    relevantTimeIn = otMark
                    releventTimeOut = mytimeout
                
                elif otMark.time() < datetime.time(22):
                    
                    relevantTimeIn = datetime.datetime.combine(otMark.date(), datetime.time(22))
                    releventTimeOut = mytimeout

            elif datetime.datetime.combine(mytimein.date(), datetime.time(22)) <= mytimeout and mytimeout >= datetime.datetime.combine((mytimein.date() + datetime.timedelta(days=1)), datetime.time(6)):
                
                if otMark.time() >= datetime.time(22) or otMark.time() <= datetime.time(6):
                    
                    relevantTimeIn = otMark
                    releventTimeOut = datetime.datetime.combine(mytimeout.date(), datetime.time(6))
                
                elif otMark.time() < datetime.time(22):
                    
                    relevantTimeIn = datetime.datetime.combine(otMark.date(), datetime.time(6))
                    releventTimeOut = mytimeout

            try:
                relevantDIFF = abs(releventTimeOut - relevantTimeIn)
            except Exception as e:
                print(e)
                relevantDIFF = datetime.timedelta(0)

            return Decimal(relevantDIFF.seconds/3600)

            # if otMark.time() >= datetime.time(22) and mytimeout.time() <= datetime.time(6):
            #     print('if_1-0-0')
            #     if mytimeout > otMark:
            #         print('if_1-1-0')
            #         if otMark.time() >= datetime.time(22) and otMark.time() <= datetime.time(6):
            #             print('if_1-1-1')
            #             relevantStart = otMark
            #             relevantEnd = mytimeout
            #         if otMark.time < datetime.time(22):
            #             print('if_1-1-2')
            #             relevantStart = datetime.datetime.combine(otMark.date(), datetime.time(22))
            #             relevantEnd = mytimeout

            # if otMark.time() >= datetime.time(22) and mytimeout.time() >= datetime.time(6):
            #     print('if_2-0-0')
            #     if mytimeout > otMark:
            #         print('if_2-1-0')
            #         if otMark.time() >= datetime.time(22) and otMark.time() <= datetime.time(6):
            #             print('if_2-1-1')
            #             relevantStart = otMark
            #             relevantEnd = datetime.datetime.combine(mytimeout.date(), datetime.time(6))
            #         if otMark.time() < datetime.time(22):
            #             print('if_2-1-2')
            #             relevantStart = datetime.datetime.combine(otMark.date(), datetime.time(22))
            #             relevantEnd = datetime.datetime.combine(mytimeout.date(), datetime.time(6))

            # relevantDIFF = abs(relevantEnd - relevantStart)

            # return Decimal(relevantDIFF.seconds/3600)


        # ACCURATE TIME IN TIME OUT COMPARISON
        # BOTH ENDS ON-TIME
        if arrival['onTime'] and departure['onTime']:
            otMark = scheduleTimeIn + datetime.timedelta(hours=9)

            print(otMark)

            bhDurationDTR = abs(otMark - scheduleTimeIn)

            bhDurationDTR = deductBreak(bhDurationDTR)
            bhDurationDTR = deductBreakNight(bhDurationDTR)

            print(bhDurationDTR)
            otDurationDTR = abs(scheduleTimeOut - otMark)
            print(otDurationDTR)

            bh += Decimal(bhDurationDTR.seconds/3600)
            ot += Decimal(otDurationDTR.seconds/3600)

            nd += getND(scheduleTimeIn, scheduleTimeOut)

            ndot += getNDOT(scheduleTimeIn, scheduleTimeOut, scheduleTimeIn, scheduleTimeOut)

            holidays = dtr.dtrdaycategory.all()
            
            restDayMarker = False
            if datetime.date.today().weekday() == 6 or (datetime.date.today().weekday() == 5 and str(datetime.date.today().weekday()) not in employee.schedule.workDays):
                restDayMarker = True
                if holidays:
                    for holiday in holidays:
                        if holiday.type == "rh":
                            rhrd += bh
                            rhrdot += ot
                            rhrdnd += nd
                            rhrdndot += ndot
                        elif holiday.type == "sh":
                            shrd += bh
                            shrdot += ot
                            shrdnd += nd
                            shrdndot += ndot
                else:
                    rd += bh
                    rdot += ot
                    rdnd += nd
                    rdndot += ndot

            if holidays and not restDayMarker:
                for holiday in holidays:
                    if holiday.type == "rh":
                        rh += bh
                        rhot += ot
                        rhnd += nd
                        rhndot += ndot
                    elif holiday.type == "sh":
                        sh += bh
                        shot += ot
                        shnd += nd
                        shndot += ndot
                    elif holiday.type == "shw":
                        shw += bh
                        shwot += ot
                        shwnd += nd
                        shwndot += ndot

            # durationDTR = scheduleTimeOut - scheduleTimeIn
            # durationDTR = deductBreak(durationDTR)

            # bh += Decimal(durationDTR.seconds/3600)

        # BOTH ENDS OFF-TIME
        elif arrival['offTime'] and departure['offTime']:
            # PSEUCODE FOR DAY SHIFT
            otMark = getOTMark(scheduleTimeIn)
            otDuration = datetime.timedelta(0)
            bhDuration = datetime.timedelta(0)

            bhDuration = abs(otMark - dtr.dateTimeIn)
            bhDuration = deductBreak(bhDuration)
            bhDuration = deductBreakNight(bhDuration)

            if dtr.dateTimeOut < otMark:
                diff = abs(otMark - dtr.dateTimeOut)
                bhDuration -= diff

            # BH IS SOLVED
            # NEXT UT
            utDuration = timeInDiff

            if datetime.time(13) <= dtr.dateTimeIn.time() <= datetime.time(17) or datetime.time(23) <= dtr.dateTimeIn.time():
                utDuration -= datetime.timedelta(hours=1)

            # AT EARLY DEPARTURE
            if otMark > dtr.dateTimeOut:
                utDuration += abs(otMark - dtr.dateTimeOut)
            # AT LATE DEPARTURE
            if otMark < dtr.dateTimeOut:
                otDuration = abs(dtr.dateTimeOut - otMark)

            nd += getND(dtr.dateTimeIn, dtr.dateTimeOut)
            ndot += getNDOT(dtr.dateTimeIn, dtr.dateTimeOut, scheduleTimeIn, scheduleTimeOut)

            bh += Decimal(bhDuration.seconds/3600)
            ot += Decimal(otDuration.seconds/3600)
            ut += Decimal(utDuration.seconds/3600)

            holidays = dtr.dtrdaycategory.all()
            
            restDayMarker = False
            if datetime.date.today().weekday() == 6 or (datetime.date.today().weekday() == 5 and datetime.date.today().weekday() in employee.schedule.workDays):
                restDayMarker = True
                if holidays:
                    for holiday in holidays:
                        if holiday.type == "rh":
                            rhrd += bh
                            rhrdot += ot
                            rhrdnd += nd
                            rhrdndot += ndot
                        elif holiday.type == "sh":
                            shrd += bh
                            shrdot += ot
                            shrdnd += nd
                            shrdndot += ndot
                else:
                    rd += bh
                    rdot += ot
                    rdnd += nd
                    rdndot += ndot

            if holidays and not restDayMarker:
                for holiday in holidays:
                    if holiday.type == "rh":
                        rh += bh
                        rhot += ot
                        rhnd += nd
                        rhndot += ndot
                    elif holiday.type == "sh":
                        sh += bh
                        shot += ot
                        shnd += nd
                        shndot += ndot
                    elif holiday.type == "shw":
                        shw += bh
                        shwot += ot
                        shwnd += nd
                        shwndot += ndot


            # durationDTR = dtr.dateTimeOut - dtr.dateTimeIn
            # durationDTR = deductBreak(durationDTR)

            # bh += Decimal(durationDTR.seconds/3600)

            # # EARLY DEPARTURE
            # if departure['earlyDeparture']:
            #     ut += Decimal(timeOutDiff.seconds/3600)

            # # LATE DEPARTURE
            # elif departure['lateDeparture']:
            #     ot += Decimal(timeOutDiff.seconds/3600)
            
            # # IF TIMEinDIFF HAS VALUE THEN WE KNOW IT'S LATE
            # ut += Decimal(timeInDiff.seconds/3600)

            # bh -=  ot

        # ARRIVAL ON-TIME ONLY
        elif arrival['onTime'] and departure['offTime']:
            # PSEUCODE FOR DAY SHIFT
            otMark = getOTMark(scheduleTimeIn)
            otDuration = datetime.timedelta(0)
            bhDuration = datetime.timedelta(0)

            bhDuration = abs(otMark - scheduleTimeIn)
            bhDuration = deductBreak(bhDuration)
            bhDuration = deductBreakNight(bhDuration)

            if dtr.dateTimeOut < otMark:
                diff = abs(otMark - dtr.dateTimeOut)
                bhDuration -= diff

            # BH IS SOLVED
            # NEXT UT
            utDuration = timeInDiff

            if datetime.time(13) <= scheduleTimeIn.time() <= datetime.time(17) or datetime.time(23) <= scheduleTimeIn.time():
                utDuration -= datetime.timedelta(hours=1)

            # AT EARLY DEPARTURE
            if otMark > dtr.dateTimeOut:
                utDuration += abs(otMark - dtr.dateTimeOut)
            # AT LATE DEPARTURE
            if otMark < dtr.dateTimeOut:
                otDuration = abs(dtr.dateTimeOut - otMark)

            nd += getND(scheduleTimeIn, dtr.dateTimeOut)
            ndot += getNDOT(scheduleTimeIn, dtr.dateTimeOut, scheduleTimeIn, scheduleTimeOut)

            bh += Decimal(bhDuration.seconds/3600)
            ot += Decimal(otDuration.seconds/3600)
            ut += Decimal(utDuration.seconds/3600)

            holidays = dtr.dtrdaycategory.all()
            
            restDayMarker = False
            if datetime.date.today().weekday() == 6 or (datetime.date.today().weekday() == 5 and datetime.date.today().weekday() in employee.schedule.workDays):
                restDayMarker = True
                if holidays:
                    for holiday in holidays:
                        if holiday.type == "rh":
                            rhrd += bh
                            rhrdot += ot
                            rhrdnd += nd
                            rhrdndot += ndot
                        elif holiday.type == "sh":
                            shrd += bh
                            shrdot += ot
                            shrdnd += nd
                            shrdndot += ndot
                else:
                    rd += bh
                    rdot += ot
                    rdnd += nd
                    rdndot += ndot

            if holidays and not restDayMarker:
                for holiday in holidays:
                    if holiday.type == "rh":
                        rh += bh
                        rhot += ot
                        rhnd += nd
                        rhndot += ndot
                    elif holiday.type == "sh":
                        sh += bh
                        shot += ot
                        shnd += nd
                        shndot += ndot
                    elif holiday.type == "shw":
                        shw += bh
                        shwot += ot
                        shwnd += nd
                        shwndot += ndot

        # DEPARTURE ON-TIME ONLY
        elif arrival['offTime'] and departure['onTime']:
            # PSEUCODE FOR DAY SHIFT
            otMark = getOTMark(scheduleTimeIn)
            otDuration = datetime.timedelta(0)
            bhDuration = datetime.timedelta(0)

            bhDuration = abs(otMark - dtr.dateTimeIn)
            bhDuration = deductBreak(bhDuration)
            bhDuration = deductBreakNight(bhDuration)

            if scheduleTimeOut < otMark:
                diff = abs(otMark - scheduleTimeOut)
                bhDuration -= diff

            # BH IS SOLVED
            # NEXT UT
            utDuration = timeInDiff

            if datetime.time(13) <= dtr.dateTimeIn.time() <= datetime.time(17) or datetime.time(23) <= dtr.dateTimeIn.time():
                utDuration -= datetime.timedelta(hours=1)

            # AT EARLY DEPARTURE FROM THE OT MARK
            if otMark > scheduleTimeOut:
                utDuration += abs(otMark - scheduleTimeOut)
            # AT LATE DEPARTURE FROM THE OT MARK
            if otMark < scheduleTimeOut:
                otDuration = abs(scheduleTimeOut - otMark)

            nd += getND(dtr.dateTimeIn, scheduleTimeOut)
            ndot += getNDOT(dtr.dateTimeIn, scheduleTimeOut, dtr.dateTimeIn, scheduleTimeOut)

            bh += Decimal(bhDuration.seconds/3600)
            ot += Decimal(otDuration.seconds/3600)
            ut += Decimal(utDuration.seconds/3600)

            holidays = dtr.dtrdaycategory.all()
            
            restDayMarker = False
            if datetime.date.today().weekday() == 6 or (datetime.date.today().weekday() == 5 and datetime.date.today().weekday() in employee.schedule.workDays):
                restDayMarker = True
                if holidays:
                    for holiday in holidays:
                        if holiday.type == "rh":
                            rhrd += bh
                            rhrdot += ot
                            rhrdnd += nd
                            rhrdndot += ndot
                        elif holiday.type == "sh":
                            shrd += bh
                            shrdot += ot
                            shrdnd += nd
                            shrdndot += ndot
                else:
                    rd += bh
                    rdot += ot
                    rdnd += nd
                    rdndot += ndot

            if holidays and not restDayMarker:
                for holiday in holidays:
                    if holiday.type == "rh":
                        rh += bh
                        rhot += ot
                        rhnd += nd
                        rhndot += ndot
                    elif holiday.type == "sh":
                        sh += bh
                        shot += ot
                        shnd += nd
                        shndot += ndot
                    elif holiday.type == "shw":
                        shw += bh
                        shwot += ot
                        shwnd += nd
                        shwndot += ndot
        
        # IF NONE OF ABOVE APPLIES
        else:
            print('something happened')


        # # UNDERTIME TIME OUT
        # if dtr.dateTimeOut < scheduleTimeOut and timeOutDiff > tolerance['default']:
        #     ut += Decimal(timeOutDiff.seconds/3600)
        #     if timeInDiff != datetime.timedelta(0):
        #         bh += Decimal(durationDTR.seconds/3600)
        #         print(bh, '1')
        #         bh = bh - ot
        #     else:
        #         bh = Decimal(8.0)
        # # OVERTIME TIME OUT
        # elif dtr.dateTimeOut < scheduleTimeOut and timeOutDiff > tolerance['afterTimeOut']:
        #     ot += Decimal(timeOutDiff.seconds/3600)
        #     if timeInDiff != datetime.timedelta(0):
        #         bh += Decimal(durationDTR.seconds/3600)

        #         print(bh, '2')
        #         bh = bh - ot
        #     else:
        #         bh = Decimal(8.0)
        # ut += Decimal(timeInDiff.seconds/3600)

        dtr.bh = bh
        dtr.ut = ut
        dtr.ot = ot
        dtr.nd = nd
        dtr.ndot = ndot
        dtr.rd = rd
        dtr.rdot = rdot
        dtr.rdnd = rdnd
        dtr.rdndot = rdndot
        dtr.rh = rh
        dtr.rhot = rhot
        dtr.rhnd = rhnd
        dtr.rhndot = rhndot
        dtr.sh = sh
        dtr.shot = shot
        dtr.shnd = shnd
        dtr.shndot = shndot
        dtr.shw = shw
        dtr.shwot = shwot
        dtr.shwnd = shwnd
        dtr.shwndot = shwndot
        dtr.rhrd = rhrd
        dtr.rhrdot = rhrdot
        dtr.rhrdnd = rhrdnd
        dtr.rhrdndot = rhrdndot
        dtr.shrd = shrd
        dtr.shrdot = shrdot
        dtr.shrdnd = shrdnd
        dtr.shrdndot = shrdndot
        dtr.save()
        
    def post(self, request, format=None):
        
        id = request.data['idNum']
        employee = User.objects.get(idUser = id)
        # try:
        try:
            employee.dtr.all().latest('pk')
            success=True

        except:
            success=False
        if success:
            if employee.dtr.all().latest('pk').dateTimeOut == None:
                self.timeOut(id)
                serializer = UserWithDTRSZ(employee)
                x = serializer.data
                x['dtr'] = serializer.data['dtr'][-1]
                return Response(x)
            else:
                self.timeIn(id, request)
                serializer = UserWithDTRSZ(employee)
                x = serializer.data
                x['dtr'] = serializer.data['dtr'][-1]
                return Response(x)
        else:
            self.timeIn(id, request)
            serializer = UserWithDTRSZ(employee)
            x = serializer.data
            print(x)
            x['dtr'] = serializer.data['dtr'][-1]
            return Response(x)
        
        