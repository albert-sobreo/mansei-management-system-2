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
router.register(r"child-nested", views.AccountChildNestedAPI, 'child-nested')

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
router.register(r"nestedmerchinventory", views.MerchandiseInventoryNestedAPI, 'nestedmerchinventory')

########## OTHER INVENTORY ##########
router.register(r"otherinventory", views.OtherInventoryAPI2, 'otherinventory')




########## ACCOUNTING APPROVALS ##########
router.register(r'purchase-order-non-approved', views.PurchaseApprovalNonApprovedAPI, 'purchase-order-non-approved')
router.register(r'purchase-order-approved', views.PurchaseApprovalApprovedAPI, 'purchase-order-approved')
router.register(r'purchase-order', views.PurchaseOrderAPI, 'purchase-order')

router.register(r'sales-contract-non-approved', views.SalesContractApprovalNonApprovedAPI, 'sales-contract-non-approved')
router.register(r'sales-contract-approved', views.SalesContractApprovalApprovedAPI, 'sales-contract-approved')

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
router.register(r"purchase-request-nested", views.PurchaseRequestNestedAPI, 'purchase-request-nested')

########## PURCHASE REQUEST ##########
router.register(r"receiving-report", views.ReceivingReportNestedAPI, 'receiving-report')

########### QUOTATIONS ###########
router.register(r"quotations", views.QuotationsAPI, 'quotations')

########### INWARD INVENTORY ###########
router.register(r"inward-inventory", views.InwardInventoryNestedAPI, 'inward-inventory')
router.register(r"inward-inventory-basic", views.InwardInventoryAPI, 'inward-inventory-basic')

########### PAYMENT VOUCHER ###########
router.register(r"payment-voucher", views.PaymentVoucherAPI, 'payment-voucher')

########## RECEIVED PAYMENT ##########
router.register(r"received-payment", views.ReceivedPaymentAPI, 'received-payment')

########## SALES INVOICE ##########
router.register(r"sales-invoice", views.SalesInvoiceAPI, 'sales-input')

########## SALES ORDER ##########
router.register(r"sales-order", views.SalesOrderAPI, 'sales-order')
 
########## SALES CONTRACT ##########
router.register(r"sales-contract", views.SalesContractAPI, 'sales-contract')

########## TRANSFER & ADJUSTMENTS ##########
router.register(r"transfer", views.TransferAPI, 'transfer')
router.register(r"adjustments", views.AdjustmentAPI, 'adjustments')

########## BRANCH DEFAULT CHILD ACCOUNT ##########
router.register(r"branch-default-child-account", views.BranchDefaultChildAccountAPI, 'branch-default-child-account')

########## PPE ##########
router.register(r"ppe", views.PPENestedAPI, "ppe")

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
    
    path('edit-account-child/<int:pk>/', login_required(views.EditChildGroup.as_view())),
    path('edit-sub-group/<int:pk>/', login_required(views.EditSubGroup.as_view())),
    path('customers/', login_required(views.CustomerView.as_view())),
    path('vendors/', login_required(views.VendorView.as_view())),
    path('save-party/', login_required(views.SaveParty.as_view())),
    path('edit-party/<int:pk>/', login_required(views.EditParty.as_view())),
    path('merchinventory/', login_required(views.MerchInventoryView.as_view())),
    path('addmerchinventory/', login_required(views.AddMerchInventoryAPI.as_view())),
    path('editmerchinventory/<int:pk>/', login_required(views.EditInventory.as_view())),
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
    path('sc-approval/<int:pk>/', login_required(views.SCApprovalAPI.as_view())),
    
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
    path('save-receivingreport/', login_required(views.SaveReceivingReport.as_view())),
    path('rr-nonapproved/', login_required(views.RRnonapproved.as_view())),
    path('rr-approved/', login_required(views.RRapproved.as_view())),
    
    path('rr-approval/<int:pk>/', login_required(views.RRApprovalAPI.as_view())),
    path('import-merch-inventory/', login_required(views.ImportMerchandiseInventory.as_view())),
    path('sales-quotations/', login_required(views.SalesQuotationsView.as_view())),
    path('sales-quotations-list/', login_required(views.QQListView.as_view())),
    path('save-quotations/', login_required(views.SaveQuotations.as_view())),
    path('qq-nonapproved/', login_required(views.QQnonapprovedView.as_view())),
    path('qq-approved/', login_required(views.QQapprovedView.as_view())),
    path('qq-approval/<int:pk>/', login_required(views.QQApprovalAPI.as_view())),
    path('inward-inventory/', login_required(views.InwardView.as_view())),
    path('import-inwardinventory/', login_required(views.ImportInwardInventory.as_view())),
    
    path('pr-approval/<int:pk>/', login_required(views.PRApprovalAPI.as_view())),
    path('inward-adjustments/', login_required(views.InwardAdjustmentsView.as_view())),
    path('save-receiving-report/', login_required(views.SaveReceivingReport.as_view())),
    path('ii-nonapproved/', login_required(views.IInonapprovedView.as_view())),
    path('ii-approved/', login_required(views.IIapprovedView.as_view())),
    path('save-inward-inventory/<int:pk>/', login_required(views.InwardAdjustmentSave.as_view())),
    path('ii-approval/<int:pk>/', login_required(views.IIApprovalAPI.as_view())),
    path('sales-order/', login_required(views.SalesOrderView.as_view())),
    path('so-list/', login_required(views.SOListView.as_view())),
    path('save-sales-order/', login_required(views.SaveSalesOrder.as_view())),
    
    path('so-nonapproved/', login_required(views.SOnonapprovedView.as_view())),
    path('so-approved/', login_required(views.SOapprovedView.as_view())),
    path('so-approval/<int:pk>/', login_required(views.SOApprovalAPI.as_view())),
    path('payment-voucher/', login_required(views.PaymentVoucherView.as_view())),
    path('save-payment-voucher/', login_required(views.SavePaymentVoucher.as_view())),
    path('pv-nonapproved/', login_required(views.PVnonapprovedView.as_view())),
    path('pv-approved/', login_required(views.PVapprovedView.as_view())),
    path('pv-approval/<int:pk>/', login_required(views.PVApprovalAPI.as_view())),
    path('sales-invoice/', login_required(views.SalesInvoiceView.as_view())),
    path('save-sales-invoice/', login_required(views.SaveSalesInvoice.as_view())),

    path('branch-profile/', login_required(views.BranchProfileView.as_view())),
    path('save-default-accounts/', login_required(views.SaveDefaultAccounts.as_view())),
    path('received-payment/', login_required(views.ReceivedPaymentView.as_view())),
    path('save-received-payment/', login_required(views.SaveReceivePayment.as_view())),
    path('import-customer-vendor/', login_required(views.ImportCustomerVendor.as_view())),
    path('transfer/', login_required(views.TransferView.as_view())),
    path('save-transfer/', login_required(views.SaveTransfer.as_view())),
    path('transfer-list/', login_required(views.TransferList.as_view())),
    path('tr-nonapproved/', login_required(views.TransferNonApproved.as_view())),
    path('tr-approved/', login_required(views.TransferApproved.as_view())),
    
    path('tr-approval/<int:pk>/', login_required(views.TransferApproval.as_view())),
    path('adjustments/', login_required(views.AdjustmentsView.as_view())),
    path('save-adjustments/', login_required(views.SaveAdjustments.as_view())),
    path('ad-nonapproved/', login_required(views.AdjustmentsNonApproved.as_view())),
    path('ad-approved/', login_required(views.AdjustmentsApproved.as_view())),
    path('ad-approval/<int:pk>/', login_required(views.AdjustmentApproval.as_view())),
    path('ad-list/', login_required(views.AdjustmentList.as_view())),
    path('delivery-list/', login_required(views.DeliveriesListView.as_view())),
    path('pr-void/<int:pk>/', login_required(views.PRVoid.as_view())),
    path('po-void/<int:pk>/', login_required(views.POVoid.as_view())),
    
    path('rr-void/<int:pk>/', login_required(views.RRVoid.as_view())),
    path('ii-void/<int:pk>/', login_required(views.IIVoid.as_view())),
    path('pv-void/<int:pk>/', login_required(views.PVVoid.as_view())),
    path('so-void/<int:pk>/', login_required(views.SOVoid.as_view())),
    path('sc-void/<int:pk>/', login_required(views.SCVoid.as_view())),
    path('rp-void/<int:pk>/', login_required(views.RPVoid.as_view())),
    path('delivery-void/<int:pk>/', login_required(views.DeliveriesVoid.as_view())),
    path('otherinventory/', login_required(views.OtherInventoryAPI.as_view())),
    path('otherinventoryview/', login_required(views.OtherInventoryView.as_view())),
    path('getaccountexpenses/', login_required(views.GetAccountExpensesAPI.as_view())),

    path('ems-dtr/', views.DTRView.as_view()),
    path('ems-list/', views.DTRList.as_view()),
    path('ems-dtr-process/', views.DTRProcess.as_view()),
    path('ems-user-w-dtr/', views.FetchUserDTR.as_view()),
    path('bank-recon/', login_required(views.BankReconView.as_view())),
    path('br-nonapproved/', login_required(views.BankReconNonApproved.as_view())),
    path('br-approved/', login_required(views.BankReconApproved.as_view())),
    path('br-approval/<int:pk>/', login_required(views.BankReconApprovalAPI.as_view())),
    path('branches/', login_required(views.BranchesView.as_view())),
    path('create-branch-in-dashboard/', login_required(views.CreateBranchInDashboard.as_view())),

    path('connect-branch-in-dashboard/', login_required(views.ConnectBranchInDashboard.as_view())),
    path('ppe/', login_required(views.PPEView.as_view())),
    path('addppe/', login_required(views.AddPPE.as_view())),
    path('import-ppe/', login_required(views.ImportPPE.as_view())),
    path('edit-ppe/<int:pk>/', login_required(views.EditPPE.as_view())),
    path('ppe-lapsing-schedule/', login_required(views.LapsingView.as_view())),
    path('ppe-update-depr/', login_required(views.UpdateDepr.as_view())),
]