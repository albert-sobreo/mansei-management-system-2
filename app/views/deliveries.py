import json
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from django.http.response import Http404

class DeliveriesView(View):
    def get(self, request, format=None):
        
        user = request.user
        context = {
            'driver-available': user.branch.driver.filter(status = 'Available'),
            'truck-available': user.branch.truck.filter(status = 'Available')
        }

        return render(request, 'deliveries.html')

class TruckView(View):
    def post(self, request, format=None):
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
        return render(request, 'trucks.html')

class DriverView(View):
    def post(self, request, format=None):
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
        return render(request, 'drivers.html')

class InTransitView(View):
    def get(self, request, format=None):
        return render(request, 'truck-in-transit.html')

class DeliveryLogsView(View):
    def get(self, request, format=None):
        return render(request, 'logs-deliveries.html')

class ReturnTruck(APIView):
    def get_object(self, pk):
        try:
            return Truck.objects.get(pk=pk)
        except Truck.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        truck = self.get_object(pk)
        truck.status = "Available"
        truck.driver.status = truck.status
        truck.driver.save()
        truck.driver = None
        truck.currentDelivery = None
        truck.save()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class SaveDelivery(APIView):
    def post(self, request, format=None):
        deliveries = request.data
        
        
        d = Deliveries()

        d.code = deliveries['code']
        d.datetimeCreated = deliveries['dateTimeCreated']
        d.truck = Truck.objects.get(pk=deliveries['truck'])
        d.driver = Driver.objects.get(pk=deliveries['driver'])

        d.truck.status = 'In-transit'
        d.truck.driver = d.driver
        d.driver.status = 'In-transit'

        d.truck.save()
        d.driver.save()

        d.save()

        d.truck.currentDelivery = d.pk
        d.truck.save()

        # for photo in photos:
        #     dp = DeliveryPhotos()
        #     dp.deliveries = d
        #     dp.picture = photo
        #     d.save()

        for dest in deliveries['destinations']:
            destination = DeliveryDestinations()
            destination.deliveries = d
            destination.destination = dest['destination']
            destination.save()

        for item in deliveries['items']:
            dItemGroup = DeliveryItemsGroup()
            dItemGroup.deliveries = d
            dItemGroup.deliveryType = item['type']
            if dItemGroup.deliveryType == 'Purchase Order':
                po = PurchaseOrder.objects.get(pk=item['code'])
                dItemGroup.referenceNo = po.code

            dItemGroup.save()

            for itemsMerch in item['transacItems']:
                poItems = POItemsMerch.objects.get(pk=itemsMerch['id'])
                
                dim = DeliveryItemMerch()
                dim.deliveryItemsGroup = dItemGroup
                dim.qty = itemsMerch['qty']
                if itemsMerch['delivered']:
                    dim.merchInventory = MerchandiseInventory.objects.get(pk=itemsMerch['code'])
                    poItems.delivered = True
                    poItems.save()


                dim.save()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)