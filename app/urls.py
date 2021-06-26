from app.views.sales import SaveQuotations
from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()

########## CHART OF ACCOUNTS ##########
router.register(r"group", views.AccountGroupAPI, 'group')
router.register(r"sub-group", views.AccountSubGroupAPI, 'sub-group')
router.register(r"child", views.AccountChildAPI, 'child')

########## LEDGER URLS ##########
router.register(r"ledger", views.LedgerAPI, 'ledger')

########## PARTY ##########
router.register(r"customer", views.CustomerAPI, 'customer')
router.register(r"customer-transaction", views.CustomerTransactionAPI, 'customer-transaction')
router.register(r"vendor", views.VendorAPI, 'vendor')
router.register(r"vendor-transaction", views.VendorTransactionAPI, 'vendor-transaction')

########## WAREHOUSE ##########
router.register(r"warehouse", views.WarehouseAPI, 'warehouse')

########## MERCH INVENTORY ##########
router.register(r"merchinventory", views.MerchandiseInventoryAPI, 'merchinvetory')

########## ACCOUNTING APPROVALS ##########
router.register(r'purchase-order-non-approved', views.PurchaseApprovalNonApprovedAPI, 'purchase-order-non-approved')
router.register(r'purchase-order-approved', views.PurchaseApprovalApprovedAPI, 'purchase-order-approved')
router.register(r'purchase-order', views.PurchaseOrderAPI, 'purchase-order')

router.register(r'sales-contract-non-approved', views.SalesContractApprovalNonApprovedAPI, 'sales-contract-non-approved')
router.register(r'sales-contract-approved', views.SalesContractApprovalApprovedAPI, 'sales-contract-approved')
router.register(r'sales-contract', views.SalesContractAPI, 'sales-contract')

########## SPECIAL TRUCK ##########
router.register(r"special-truck", views.SpecialTruckAPI, 'special-truck')

########## DELIVERIES ##########
router.register(r"deliveries", views.DeliveriesAPI, 'deliveries')

########## ATC ##########
router.register(r"atc", views.ATCAPI, 'atc')

########## PURCHASE ORDER ##########
router.register(r"purchase-order-approved", views.PurchaseOrderApprovedAPI, 'purchase-order-approved')

########## PURCHASE REQUEST ##########
router.register(r"purchase-request", views.PurchaseRequestAPI, 'purchase-request')
router.register(r"purchase-request-non-approved", views.PurchaseRequestNonApprovedAPI, 'purchase-request-non-approved')
router.register(r"purchase-request-approved", views.PurchaseRequestApprovedAPI, 'purchase-request-approved')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('', login_required(views.DashboardView.as_view())),
    path('chart-of-accounts/', login_required(views.ChartOfAccountsView.as_view())),
    path('journal/', login_required(views.JournalView.as_view())),
    path('save-journal/', login_required(views.SaveJournal.as_view())),
    path('ledger/', login_required(views.LedgerView.as_view())),
    path('save-account-child/', login_required(views.SaveAccountChild.as_view())),
    path('save-account-group/', login_required(views.SaveAccountGroup.as_view())),
    path('customers/', login_required(views.CustomerView.as_view())),
    path('vendors/', login_required(views.VendorView.as_view())),
    path('save-party/', login_required(views.SaveParty.as_view())),
    path('merchinventory/', login_required(views.MerchInventoryView.as_view())),
    path('addmerchinventory/', login_required(views.AddMerchInventoryAPI.as_view())),
    path('warehouse/', login_required(views.WarehouseView.as_view())),
    path('addwarehouse/', login_required(views.AddWarehoseAPI.as_view())),
    path('purchase-request/', login_required(views.PurchaseRequestView.as_view())),
    path('pr-list/', login_required(views.PRListView.as_view())),
    path('save-purchase-request/', login_required(views.SavePurchaseRequest.as_view())),
    path('pr-nonapproved/', login_required(views.PRnonapprovedView.as_view())),
    path('pr-approved/', login_required(views.PRapprovedView.as_view())),
    path('purchase-order/', login_required(views.PurchaseOrderView.as_view())),
    path('po-list/', login_required(views.POListView.as_view())),
    path('save-purchase-order/', login_required(views.SavePurchaseOrder.as_view())),
    path('po-nonapproved/', login_required(views.POnonapprovedView.as_view())),
    path('po-approved/', login_required(views.POapprovedView.as_view())),
    path('po-approval/<int:pk>/', login_required(views.POApprovalAPI.as_view())),
    path('purchase-order-list/', login_required(views.POListView.as_view())),
    path('sales-contract/', login_required(views.SalesContractView.as_view())),
    path('sc-list/', login_required(views.SCListView.as_view())),
    path('save-sales-contract/', login_required(views.SaveSalesContract.as_view())),
    path('sc-nonapproved/', login_required(views.SCnonapprovedView.as_view())),
    path('sc-approved/', login_required(views.SCapprovedView.as_view())),
    path('sales-contract-list/', login_required(views.SCListView.as_view())),
    path('sales-contract/<int:pk>/', login_required(views.SCApprovalAPI.as_view())),
    path('deliveries/', login_required(views.DeliveriesView.as_view())),
    path('trucks/', login_required(views.TruckView.as_view())),
    path('drivers/', login_required(views.DriverView.as_view())),
    path('truck-in-transit/', login_required(views.InTransitView.as_view())),
    path('delivery-logs/', login_required(views.DeliveryLogsView.as_view())),
    path('return-truck/', login_required(views.ReturnTruck.as_view())),
    path('save-delivery/', login_required(views.SaveDelivery.as_view())),
    path('in-transit/', login_required(views.InTransitView.as_view())),
    path('deliveriesnonapproved/', login_required(views.DeliveriesNonApproved.as_view())),
    path('deliveriesapproved/', login_required(views.DeliveriesApproved.as_view())),
    path('approve-deliveries/<int:pk>/', login_required(views.DeliveriesApprovalAPI.as_view())),
    path('return-truck/<int:pk>/', login_required(views.ReturnTruck.as_view())),
    path('import-atc/', login_required(views.ImportATC.as_view())),
    path('purchase-request/', login_required(views.PurchaseRequestView.as_view())),
    path('getvendorquotes/', login_required(views.VendorQuotes.as_view())),
    path('receiving-report/', login_required(views.ReceivingReportView.as_view())),
    path('rr-list/', login_required(views.RRListView.as_view())),
    path('rr-nonapproved/', login_required(views.RRnonapproved.as_view())),
    path('rr-approved/', login_required(views.RRapproved.as_view())),
    path('rr-approval/<int:pk>/', login_required(views.RRApprovalAPI.as_view())),
    path('import-merch-inventory/', login_required(views.ImportMerchandiseInventory.as_view())),
    path('sales-quotations/', login_required(views.SalesQuotationsView.as_view())),
    path('sales-quotations-list/', login_required(views.QQListView.as_view())),
    path('save-quotations/', login_required(views.SaveQuotations.as_views())),
    path('qq-nonapproved/', login_required(views.QQnonapprovedView.as_view())),
    path('qq-approved/', login_required(views.QQapprovedView.as_view())),
    path('qq-approval/<int:pk>/', login_required(views.QQApprovalAPI.as_view())),
    path('inward-inventory/', login_required(views.InwardView.as_view()))
]