from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path, include

from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()

########## NOTIFICATIONS ##########
router.register(r"notifications", views.NotificationsAPI, 'notifications')

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
router.register(r"warehouse-nested", views.WarehouseNestedAPI, 'warehouse-nested')

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
router.register(r'receiving-report-approved', views.ReceivingReportNestedApprovedAPI, 'receiving-report-approved')

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
router.register(r"ppe-real", views.PPEAPI, 'ppe-real')

########## CR ##########
router.register(r"cr-nested", views.CRNestedAPI, 'cr-nested')

########## OT ##########
router.register(r'ot-request', views.OTRequestAPI, 'ot-request')

########## UT ##########
router.register(r'ut-request', views.UTRequestAPI, 'ut-request')

########## PAYROLL ##########
router.register(r'complex-payroll', views.ComplexPayrollAPI, 'complex-payroll')
router.register(r"payroll", views.PayrollAPI, 'payroll')

########## USER ##########
router.register(r'user', views.UserAPI, 'user')
router.register(r'user2', views.UserAPI2, 'user2')
router.register(r'user-payrollable', views.UserPayrollableAPI, 'user-payrollable')
router.register(r'user-w-13', views.UserWith13thAPI, 'user-w-13')

########## DE MINIMIS ##########
router.register(r'deminimis', views.DeMinimisAPI, 'user')

########## DTR ##########
router.register(r'user-w-dtr', views.UserWithDTRAPI, 'user-w-dtr')

########## HOLIDAY ##########
router.register(r"holiday", views.HolidayAPI, 'holiday')

########## PETTY CASH ##########
router.register(r"advancement", views.AdvancementAPI, 'advancement')
router.register(r"user-advancements", views.UsersAdvancementsAPI, 'user-advancements')

########## PROJECT PLANNING ##########
router.register(r"project-assignee", views.ProjectAssigneeAPI, "project-assignee")
router.register(r"project-task", views.ProjectTaskAPI, "project-task")
router.register(r"project-task-nested", views.ProjectTaskNestedAPI, "project-task-nested")
router.register(r"project-stage", views.ProjectStageAPI, "project-stage")
router.register(r"project-stage-nested", views.ProjectStageNestedAPI, "project-stage-nested")
router.register(r"project-plan", views.ProjectPlanAPI, "project-plan")
router.register(r"project-plan-nested", views.ProjectPlanNestedAPI, "project-plan-nested")
router.register(r"project-department", views.ProjectDepartmentAPI, "project-department")
router.register(r"project-department-nested", views.ProjectDepartmentNestedAPI, "project-department-nested")
router.register(r"assignee", views.AssigneeAPI, 'assignee')

########## BRANCH LIST ##########
router.register(r"branch-list", views.BranchListAPI, 'branch-list')

########## LIQUIDATION ##########
router.register(r"liquidation", views.LiquidationAPI, 'liquidation')

########## EXPORTS ##########
router.register(r"exports", views.ExportsAPI, 'exports')
router.register(r"receivepaymentsUSD", views.ReceivedPaymentsUSDAPI, 'receivepaymentsUSD')

########## JOB ORDER ##########
router.register(r"job-order", views.JobOrderAPI, 'job-order')
router.register(r"job-order-2", views.JobOrderAPI2, 'job-order-2')

########## MANUFACTURING INVENTORY ##########
router.register(r'manufacturing-inventory', views.ManufacturingInventoryAPI, 'manufacturing-inventory')

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
    path('delete-merch-inventory/<int:pk>/', login_required(views.DeleteMerchInventory.as_view())),
    path('chart-of-accounts-subgroup/', login_required(views.SubGroupView.as_view())),
    path('chart-of-accounts-group/', login_required(views.GroupView.as_view())),
    
    path('edit-group/<int:pk>/', login_required(views.EditGroup.as_view())),
    path('reset-accounts/', login_required(views.ResetChartOfAccounts.as_view())),
    path('reset-account-process/', login_required(views.ResetChartOfAccountsProcess.as_view())),
    path('upload-test/', login_required(views.UploadView.as_view())),
    path('completion-report/', login_required(views.CompletionReportView.as_view())),
    path('cr-list/', login_required(views.CRList.as_view())),
    path('po-repair/', login_required(views.PurchaseOrderApprovedRepairAPI.as_view())),
    path('cr-nonapproved/', login_required(views.CRnonapproved.as_view())),
    path('cr-approved/', login_required(views.CRapproved.as_view())),
    path('cr-approval/<int:pk>/', login_required(views.CRApproval.as_view())),
    
    path('cr-success/<int:pk>/', login_required(views.CRSuccessUpdate.as_view())),
    path('cr-incomplete/<int:pk>/', login_required(views.CRIncompleteUpdate.as_view())),
    path('cr-transaction/<int:pk>/', login_required(views.CRTransactionUpdate.as_view())),
    path('cr-capitalize/<int:pk>/', login_required(views.CRCapitalize.as_view())),
    path('ems-my-dtr/', login_required(views. EMS_MyDTRView.as_view())),
    path('ems-employee-dtr/', login_required(views.EMS_EmployeeDTRView.as_view())),
    path('ems-my-timesheet/', login_required(views.EMS_MyTimesheetView.as_view())),
    path('year-api/', login_required(views.ReturnYearsView.as_view())),
    path('ems-employee-timesheet/', login_required(views.EMS_EmployeeTimesheetView.as_view())),
    path('ems-timesheet-tabular/', login_required(views.EMS_TimesheetTabularView.as_view())),

    path('ems-my-payslip/', login_required(views.EMS_MyPayslipView.as_view())),
    path('ems-employee-payslip/', login_required(views.EMS_EmployeePayslipView.as_view())),
    path('ems-payroll/', login_required(views.EMS_PayrollView.as_view())),
    path('ems-holidays/', login_required(views.EMS_HolidaysView.as_view())),
    path('ems-employees/', login_required(views.EMS_EmployeesView.as_view())),
    path('ems-raise-history/', login_required(views.EMS_RaiseHistoryView.as_view())),
    path('ems-overtime-request/', login_required(views.EMS_OvertimeRequestsView.as_view())),
    path('ems-undertime-request/', login_required(views.EMS_UndertimeRequestsView.as_view())),
    path('ems-leave-request/', login_required(views.EMS_LeaveRequestsView.as_view())),
    path('ems-overtime-pending/', login_required(views.EMS_OvertimePendingView.as_view())),
    
    path('ems-overtime-approved/', login_required(views.EMS_OvertimeApprovedView.as_view())),
    path('ems-overtime-approval/<int:pk>/', login_required(views.EMS_OvertimeApproval.as_view())),
    path('ems-overtime-disapproval/<int:pk>/', login_required(views.EMS_OvertimeDisapproval.as_view())),
    path('ems-undertime-pending/', login_required(views.EMS_UndertimePendingView.as_view())),
    path('ems-undertime-approved/', login_required(views.EMS_UndertimeApprovedView.as_view())),
    path('ems-undertime-approval/<int:pk>/', login_required(views.EMS_UndertimeApproval.as_view())),
    path('ems-undertime-disapproval/<int:pk>/', login_required(views.EMS_UndertimeDisapproval.as_view())),
    path('ems-leave-pending/', login_required(views.EMS_LeavePendingView.as_view())),
    path('ems-leave-approved/', login_required(views.EMS_LeaveApprovedView.as_view())),
    path('ems-leave-approval/<int:pk>/', login_required(views.EMS_LeaveApproval.as_view())),
    
    path('ems-leave-disapproval/<int:pk>/', login_required(views.EMS_LeaveDisapproval.as_view())),
    path('ems-import-holidays/', login_required(views.EMS_ImportHolidays.as_view())),
    path('import-chart-of-accounts/', login_required(views.ImportChartOfAccounts.as_view())),
    path('ems-generate-payroll/', login_required(views.EMS_GeneratePayroll.as_view())),
    path('ems-edit-timesheet-hours/<int:pk>/<int:fromPage>/<str:params>/', login_required(views.EMS_EditTimesheetHours.as_view())),
    path('contribution-profile/', login_required(views.PayrollContributionsView.as_view())),
    path('import-sss/', login_required(views.ImportSSSContributions.as_view())),
    path('import-phic/', login_required(views.ImportPHICContributions.as_view())),
    path('income-tax-deductions/', login_required(views.IncomeTaxDeductionProfile.as_view())),
    path('give-deminimis/', login_required(views.GiveDeMinimis.as_view())),

    path('ems-edit-payroll/', login_required(views.EMS_EditPayrollView.as_view())),
    path('ems-edit-payroll-save/<int:pk>/', login_required(views.EMS_EditPayrollSave.as_view())),
    path('ems-payroll-approval-all/', login_required(views.EMS_PayrollApprovalAll.as_view())),
    path('ems-save-edit-leave/', login_required(views.EMS_SaveEditLeave.as_view())),
    path('ems-give-raise/', login_required(views.EMS_GiveRaise.as_view())),
    path('ems-save-edit-holiday/', login_required(views.EMS_SaveEditHoliday.as_view())),
    path('branch-positions/', login_required(views.BranchPositions.as_view())),
    path('ems-give-promotion/', login_required(views.EMS_GivePromotion.as_view())),
    path('ems-deduction-sss/', login_required(views.EMS_SSSDeductionView.as_view())),
    path('ems-deduction-phic/', login_required(views.EMS_PHICDeductionView.as_view())),

    path('ems-deduction-hdmf/', login_required(views.EMS_HDMFDeduction.as_view())),
    path('ems-deduction-taxes/', login_required(views.EMS_TaxDeduction.as_view())),
    path('ems-loans-sss/', login_required(views.EMS_SSSLoansView.as_view())),
    path('ems-deduction-sss-loans/', login_required(views.EMS_SSSLoanDeduction.as_view())),
    path('ems-loan-create/', login_required(views.EMS_LoanCreate.as_view())),
    path('ems-loans-hdmf/', login_required(views.EMS_HDMFLoansView.as_view())),
    path('ems-save-edit-benefits/', login_required(views.EMS_SaveEditBenefits.as_view())),
    path('pps-planner/', login_required(views.PPS_ProjectPlannerView.as_view())),
    path('pps-add-department/', login_required(views.PPS_AddDepartment.as_view())),
    path('pps-add-project/', login_required(views.PPS_AddProject.as_view())),

    path('pps-add-stage/', login_required(views.PPS_AddStage.as_view())),
    path('pps-add-task/', login_required(views.PPS_AddTask.as_view())),
    path('pps-save-edit-stage/', login_required(views.PPS_SaveEditStage.as_view())),
    path('pps-delete-stage/', login_required(views.PPS_DeleteEditStage.as_view())),
    path('pps-save-edit-task/', login_required(views.PPS_SaveEditTask.as_view())),
    path('pps-delete-task/', login_required(views.PPS_DeleteEditTask.as_view())),
    path('pps-save-edit-department/', login_required(views.PPS_SaveEditDepartment.as_view())),
    path('pps-save-edit-project/', login_required(views.PPS_SaveEditProject.as_view())),
    path('pps-delete-project/', login_required(views.PPS_DeleteEditProject.as_view())),
    path('my-profile/', login_required(views.MyProfileView.as_view())),

    path('save-my-profile-picture/', login_required(views.MyProfileSaveProfilePicture.as_view())),
    path('save-my-profile-personal-info/', login_required(views.MyProfileSavePersonalInfo.as_view())),
    path('save-my-profile-employee-info/', login_required(views.MyProfileSaveEmployeeInfo.as_view())),
    path('save-my-profile-password/', login_required(views.MyProfileSavePassword.as_view())),
    path('save-my-profile-email/', login_required(views.MyProfileSaveEmail.as_view())),
    path('qr-generator/', login_required(views.QRGeneratorView.as_view())),
    path('total-bonus-of-user-for-current-year/', login_required(views.TotalBonusOfUserForCurrentYearAPI.as_view())),
    path('move-task-to-stage/', login_required(views.MoveTaskToStage.as_view())),
    path('dashboard-data/', login_required(views.DashboardAPI.as_view())),
    path('save-notepad/', login_required(views.SaveNotepad.as_view())),

    path('save-announcement/', login_required(views.SaveAnnouncement.as_view())),
    path('delete-announcement/', login_required(views.DeleteAnnouncement.as_view())),
    path('test-export/', login_required(views.ExcelReportAPI.as_view())),
    path('annualization-export/', login_required(views.GenerateAnnualizationView.as_view())),
    path('add-bonus/', login_required(views.PayrollAddBonus.as_view())),
    path('generate-13th/', login_required(views.Give13thMonthPay.as_view())),
    path('ems-13th/', login_required(views.EMS_13thMonthView.as_view())),
    path('generate-13th-individual/', login_required(views.Give13thMonthPayIndividual.as_view())),
    path('admin-dashboard/', login_required(views.AdminDashboardView.as_view())),
    path('admin-change-user-branch/', login_required(views.AdminChangeUserBranch.as_view())),

    path('gas-advancements/', login_required(views.GAS_AdvancementsView.as_view())),
    path('save-advancements/', login_required(views.SaveAdvancement.as_view())),
    path('adv-nonapproved/', login_required(views.ADVnonapproved.as_view())),
    path('adv-approved/',login_required(views.ADVapproved.as_view())),
    path('adv-approval/', login_required(views.ADVapprovalAPI.as_view())),
    path('petty-cash/', login_required(views.PettyCashView.as_view())),
    path('replenish-petty-cash/', login_required(views.PettyCashReplenish.as_view())),
    path('save-edit-default-petty-cash-fund/', login_required(views.SaveDefaultPettyCash.as_view())),
    path('liquidation-form/', login_required(views.LiquidationView.as_view())),
    path('save-liquidation-form/', login_required(views.SaveLiquidationForm.as_view())),

    path('liquidation-list/', login_required(views.LiquidationListView.as_view())),
    path('lqd-nonapproved/', login_required(views.LQDnonapproved.as_view())),
    path('lqd-approved/', login_required(views.LQDapproved.as_view())),
    path('lqd-approval/', login_required(views.LiquidationApprovalAPI.as_view())),
    path('return-advancement/', login_required(views.ReturnAdvancement.as_view())),
    path('delete-advancement/', login_required(views.ADVDeleteAPI.as_view())),
    path('2307/', login_required(views.BIR2307View.as_view())),
    path('0619-E/', login_required(views.BIR0619EView.as_view())),
    path('1601-C/', login_required(views.BIR1601CView.as_view())),
    path('1702-Q/', login_required(views.BIR1702QView.as_view())),

    path('reimbursement/', login_required(views.ReimbursementView.as_view())),
    path('reimburse-process/', login_required(views.ReimbursementProcess.as_view())),
    path('add-employee/', login_required(views.EMS_AddEmployee.as_view())),
    path('1601-EQ/', login_required(views.BIR1601EQView.as_view())),
    path('2316/', login_required(views.BIR2316View.as_view())),
    path('balance-sheet/', login_required(views.BalanceSheetView.as_view())),
    path('balance-sheet-request/', login_required(views.BalanceSheetRequest.as_view())),
    path('income-statement/', login_required(views.IncomeStatementView.as_view())),
    path('income-statement-request/', login_required(views.IncomeStatementRequest.as_view())),
    path('cash-flow/', login_required(views.CashFlowView.as_view())),

    path('cash-flow-request/', login_required(views.CashFlowRequest.as_view())),
    path('void-journal/<int:pk>/', login_required(views.VoidJournal.as_view())),
    path('exports/', login_required(views.ExportsView.as_view())),
    path('exports-list/', login_required(views.ExportsListView.as_view())),
    path('save-exports/', login_required(views.SaveExports.as_view())),
    path('received-payments-usd/', login_required(views.ReceivedPaymentsUSDView.as_view())),
    path('save-received-payments-usd/', login_required(views.SaveReceivePaymentsUSD.as_view())),
    path('exports-nonapproved/', login_required(views.Exportsnonapproved.as_view())),
    path('exports-approved/', login_required(views.Exportsapproved.as_view())),
    path('exports-approval/', login_required(views.ExportsApprovalAPI.as_view())),

    path('html-to-excel/', login_required(views.HTMLtoEXCELView.as_view())),
    path('job-order/', login_required(views.JobOrderView.as_view())),
    path('create-job-order/', login_required(views.CreateJobOrderAPI.as_view())),
    path('job-order-nonapproved/', login_required(views.JobOrdernonapproved.as_view())),
    path('job-order-approved/', login_required(views.JobOrderapproved.as_view())),
    path('job-order-approval/', login_required(views.JobOrderApprovalAPI.as_view())),
    path('export-sales-order/<int:pk>/', login_required(views.ExportSO.as_view())),
    path('export-sales-contract/<int:pk>/', login_required(views.ExportSC.as_view())),
    path('export-dr-ls/<int:pk>/', login_required(views.ExportDRLS.as_view())),
    path('export-quotations-slip/<int:pk>/', login_required(views.ExportQuotationsSlip.as_view())),

    path('job-order-ongoing/', login_required(views.JobOrderOnGoingView.as_view())),
    path('job-order-finished/', login_required(views.JobOrderFinishedView.as_view())),
    path('edit-job-order/', login_required(views.EditJobOrder.as_view())),
    path('job-order-edit-on-going/', login_required(views.EditJobOrderView.as_view())),
    path('finish-job-order/', login_required(views.JobOrderFinish.as_view())),
    path('export-commercial-invoice/<int:pk>/', login_required(views.ExportCompercialInvoice.as_view())),
    path('export-packing-list/<int:pk>/', login_required(views.ExportPackingList.as_view())),
    path('notifications/<int:pk>/', login_required(views.NotificationReceiver.as_view())),
    path('notification-unread-checker/', login_required(views.NotificationUnreadChecker.as_view())),

    path('manuInventory/', login_required(views.ManuInventoryView.as_view())),
    path('save-edit-manu-inventory/', login_required(views.SaveEditManuInventoryAPI.as_view())),
    path('save-change-schedule/', login_required(views.SaveChangeSchedule.as_view())),
    path('create-schedule/', login_required(views.CreateScheduleAPI.as_view()))
]   