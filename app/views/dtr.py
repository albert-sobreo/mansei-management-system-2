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

class DTRList(View):
    def get(self, request, format=None):
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

        return render(request, 'ems-dtr.html')

# RETURN MESSAGES
# 0 - SUCCESS
# 1 - DID NOT TIMEOUT

class DTRProcess(APIView):
    def timeIn(self, userID):
        employee = User.objects.get(idUser=userID)
        
        dtr = DTR()
        dtr.dateTimeIn = datetime.datetime.now()
        dtr.user = employee
        dtr.date = datetime.date.today()
        dtr.save()
    
    # def timeOut(self, userID):
    #     employee = User.objects.get(idUser=userID)
    
    #     dtr = employee.dtr.all().latest('pk')
    #     dtr.dateTimeOut = datetime.datetime.now()
    #     dtr.save()

    #     rh = Decimal(0)
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

        rh = Decimal(0)
        ut = Decimal(0)
        ot = Decimal(0)
        
        tolerance = {
            'default': datetime.timedelta(minutes=5),
            'afterTimeOut': datetime.timedelta(minutes=30)
        }

        breakStart = datetime.datetime.combine(datetime.date.today(), datetime.time(12))
        breakEnd = datetime.datetime.combine(datetime.date.today(), datetime.time(13))

        scheduleTimeIn = datetime.datetime.combine(datetime.date.today(), employee.schedule.timeIn)
        scheduleTimeOut = datetime.datetime.combine(datetime.date.today(), employee.schedule.timeOut)

        # durationSchedule = scheduleTimeOut - scheduleTimeIn - datetime.timedelta(hours=1) #timedelta
        
        # durationDiff = abs(durationSchedule - durationDTR)
        

        timeInDiff = abs(scheduleTimeIn - dtr.dateTimeIn) #timedelta
        timeOutDiff = abs(scheduleTimeOut - dtr.dateTimeOut) #timedelta

        # EARLY OR ON TIME
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

        # A FUNCTION TO DEDUCT BREAK FROM DURATION DTR
        def deductBreak(time):
            return time - datetime.timedelta(hours=1) if dtr.dateTimeOut >= breakEnd and dtr.dateTimeIn <= breakStart else time


        # ACCURATE TIME IN TIME OUT COMPARISON
        # BOTH ENDS ON-TIME
        if arrival['onTime'] and departure['onTime']:
            durationDTR = scheduleTimeOut - scheduleTimeIn
            durationDTR = deductBreak(durationDTR)

            rh += Decimal(durationDTR.seconds/3600)

        # BOTH ENDS OFF-TIME
        elif arrival['offTime'] and departure['offTime']:
            durationDTR = dtr.dateTimeOut - dtr.dateTimeIn
            durationDTR = deductBreak(durationDTR)

            rh += Decimal(durationDTR.seconds/3600)

            # EARLY DEPARTURE
            if departure['earlyDeparture']:
                ut += Decimal(timeOutDiff.seconds/3600)

            # LATE DEPARTURE
            elif departure['lateDeparture']:
                ot += Decimal(timeOutDiff.seconds/3600)
            
            # IF TIMEinDIFF HAS VALUE THEN WE KNOW IT'S LATE
            ut += Decimal(timeInDiff.seconds/3600)

            rh -=  ot

        # ARRIVAL ON-TIME ONLY
        elif arrival['onTime'] and departure['offTime']:
            durationDTR = dtr.dateTimeOut - scheduleTimeIn
            durationDTR = deductBreak(durationDTR)

            rh += Decimal(durationDTR.seconds/3600)

            # EARLY DEPARTURE
            if departure['earlyDeparture']:
                ut += Decimal(timeOutDiff.seconds/3600)

            # LATE DEPARTURE
            elif departure['lateDeparture']:
                ot += Decimal(timeOutDiff.seconds/3600)

            rh -=  ot

        # DEPARTURE ON-TIME ONLY
        elif arrival['offTime'] and departure['onTime']:
            durationDTR = scheduleTimeOut - dtr.dateTimeIn
            durationDTR = deductBreak(durationDTR)

            rh += Decimal(durationDTR.seconds/3600)

            ut += Decimal(timeInDiff.seconds/3600)
        
        # IF NONE OF ABOVE APPLIES
        else:
            print('something happened')


        # # UNDERTIME TIME OUT
        # if dtr.dateTimeOut < scheduleTimeOut and timeOutDiff > tolerance['default']:
        #     ut += Decimal(timeOutDiff.seconds/3600)
        #     if timeInDiff != datetime.timedelta(0):
        #         rh += Decimal(durationDTR.seconds/3600)
        #         print(rh, '1')
        #         rh = rh - ot
        #     else:
        #         rh = Decimal(8.0)
        # # OVERTIME TIME OUT
        # elif dtr.dateTimeOut < scheduleTimeOut and timeOutDiff > tolerance['afterTimeOut']:
        #     ot += Decimal(timeOutDiff.seconds/3600)
        #     if timeInDiff != datetime.timedelta(0):
        #         rh += Decimal(durationDTR.seconds/3600)

        #         print(rh, '2')
        #         rh = rh - ot
        #     else:
        #         rh = Decimal(8.0)
        # ut += Decimal(timeInDiff.seconds/3600)

        dtr.rh = rh
        dtr.ut = ut
        dtr.ot = ot
        dtr.save()
        
    def post(self, request, format=None):
        
        id = request.data['idNum']
        employee = User.objects.get(idUser = id)
        try:   
            if employee.dtr.all().latest('pk').dateTimeOut == None:
                self.timeOut(id)
                serializer = UserWithDTRSZ(employee)
                x = serializer.data
                x['dtr'] = serializer.data['dtr'][-1]
                return Response(x)
            else:
                self.timeIn(id)
                serializer = UserWithDTRSZ(employee)
                x = serializer.data
                x['dtr'] = serializer.data['dtr'][-1]
                return Response(x)
        except Exception as e:
            print(e)
            self.timeIn(id)
            serializer = UserWithDTRSZ(employee)
            x = serializer.data
            print(x)
            x['dtr'] = serializer.data['dtr'][-1]
            return Response(x)
        
        