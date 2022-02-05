import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from django.http.response import Http404
from datetime import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class DeliveriesView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        user = request.user

        try:
            d = user.branch.deliveries.latest('pk')

            listed_code = d.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'D-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'D-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'D-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'driverAvailable': user.branch.driver.filter(status = 'Available'),
            'truckAvailable': user.branch.truck.filter(status = 'Available'),
            'new_code': new_code
        }

        return render(request, 'deliveries.html', context)

class DeliveriesListView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'delivery-list.html')

class TruckView(View):
    def post(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        request.data = json.loads(request.body)
        jsonTruck = request.data

        truck = Truck()

        truck.plate = jsonTruck['plate']
        truck.brand = jsonTruck['brand']
        truck.model = jsonTruck['model']
        truck.status = jsonTruck['status']

        truck.save()
        request.user.branch.truck.add(truck)

        sweetify.sweetalert(request, icon="success", title="Success!", text="{} {} with plate {} has been added as truck.".format(truck.brand, truck.model, truck.plate), persistent="Dismiss")
        return JsonResponse(0, safe=False)

    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'trucks.html')

class DriverView(View):
    def post(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        request.data = json.loads(request.body)
        jsonDriver = request.data

        driver = Driver()

        driver.driverID = jsonDriver['driverID']
        driver.firstName = jsonDriver['firstName']
        driver.lastName = jsonDriver['lastName']
        driver.status = jsonDriver['status']

        driver.save()
        request.user.branch.driver.add(driver)

        sweetify.sweetalert(request, icon="success", title="Success!", text="{} {} with ID of {} has been added as driver.".format(driver.firstName, driver.lastName, driver.driverID), persistent="Dismiss")
        return JsonResponse(0, safe=False)

    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'drivers.html')

class InTransitView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'trucks': request.user.branch.truck.filter(status='In-transit')
        }
        return render(request, 'truck-in-transit.html', context)

class DeliveryLogsView(View):
    def get(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'logs-deliveries.html')

class ReturnTruck(APIView):
    def get_object(self, request, pk):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        try:
            return Truck.objects.get(pk=pk)
        except Truck.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        truck = self.get_object(pk)
        truck.status = "Available"
        truck.driver.status = truck.status
        truck.driver.save()
        truck.driver = None
        truck.currentDelivery = None
        truck.save()
        notify(request, 'Truck Returned', f'{truck.plate} has returned', '/trucks/', 1)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SaveDelivery(APIView):
    def post(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        deliveries = request.data
        
        d = Deliveries()

        d.code = deliveries['code']
        d.datetimeCreated = datetime.now()
        d.truck = Truck.objects.get(pk=deliveries['truck'])
        d.driver = Driver.objects.get(pk=deliveries['driver'])
        d.scheduleStart = deliveries['scheduleStart']
        d.scheduleEnd = deliveries['scheduleEnd']
        d.amountTotal = deliveries['amountTotal']
        if request.user.is_authenticated:
            d.createdBy = request.user


        d.save()
        request.user.branch.deliveries.add(d)

        for item in deliveries['items']:
            dig = DeliveryItemsGroup()
            dig.deliveries = d
            dig.deliveryType = item['type']
            dig.referenceNo = item['code']
            dig.save()
            request.user.branch.deliveryitemsGroup.add(dig)

            


            for itemMerch in item['transacItems']:
                if itemMerch['delivered']:
                    if item['type'] == 'Sales Contract':
                        scitemsmerch = SCItemsMerch.objects.get(pk=itemMerch['id'])
                        scitemsmerch.delivered = True
                        scitemsmerch.save()
                    dim = DeliveryItemMerch()
                    dim.deliveryItemsGroup = dig
                    dim.merchInventory = MerchandiseInventory.objects.get(pk=itemMerch['code'])
                    dim.qty = itemMerch['qty']
                    dim.save()
                    request.user.branch.deliveryitemsMerch.add(dim)
        
        for dest in deliveries['destinations']:
            destination = DeliveryDestinations()
            destination.deliveries = d
            destination.destination = dest['destination']
            destination.save()
            request.user.branch.deliveriesDestination.add(destination)
        notify(request, 'New Deliveries', d.code, '/deliveriesnonapproved/', 1)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)