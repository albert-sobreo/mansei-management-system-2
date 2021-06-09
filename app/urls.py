from django.contrib import admin
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
    path('purchase-order/', login_required(views.PurchaseOrderView.as_view())),
    path('po-list/', login_required(views.POListView.as_view())),
    path('save-purchase-order/', login_required(views.SavePurchaseOrder.as_view())),
    path('po-nonapproved/', login_required(views.POnonapprovedView.as_view())),
    path('po-approved/', login_required(views.POapprovedView.as_view())),
    path('po-approval/<int:pk>/', login_required(views.POApprovalAPI.as_view())),
    path('sales-contract/', login_required(views.SalesContractView.as_view())),
    path('sc-list/', login_required(views.SCListView.as_view())),
    path('save-sales-contract/', login_required(views.SaveSalesContract.as_view())),
    path('sc-nonapproved/', login_required(views.SCnonapprovedView.as_view())),
    path('sc-approved/', login_required(views.SCapprovedView.as_view())),
]