Vue.component('navbar-gas', {
    delimiters: ['[[', ']]'],
    props: [
        'active',
        'photo'
    ],
    data(){
        return {
            
            const:{
                iconSelector: '/static/media/icons/iconselector.svg',
                bellIcon: '/static/media/icons/bell-solid 1.svg',
                gasLogo: '/static/media/icons/GAS.svg',
                impsLogo: '/static/media/icons/imps.svg',
                emsLogo: '/static/media/icons/EMS.svg',
                dashboardLogo: '/static/media/icons/Dashboard.svg',
                hrefProfile: '/static/media/icons/person.png'
            }
        }
    },
    mounted(){
        var x = document.getElementById(this.active)
        x.classList.add('active-gas')
    },
    
    template: /*javascript*/`
    <div class="c-nav d-flex mb-3 font-bold" id="main-nav">
        <!-- LOGO CONTAINER -->
        <div class="c-nav-item justify-content-start">
            <img :src='this.const.gasLogo' class="logo">
        </div>

        <!-- TABS CONTAINER -->
        <div class="gas-nav justify-content-center font-semibold navbar">
            <a href="/journal/" class="mx-3" id="nav-journal">Journal</a>
            <div class="btn-group mx-3">
                <a id="nav-sales" href="#" class="" data-toggle="dropdown">Sales</a>
                <div class="dropdown-menu b-radius-5 py-0">
                    <a href="/sales-quotations/" class="dropdown-item d-item-gas font-size-12 font-semibold">Quotations</a>
                    <a href="/sales-order/" class="dropdown-item d-item-gas font-size-12 font-semibold">Sales Order</a>
                    <a href="/sales-contract/" class="dropdown-item d-item-gas font-size-12 font-semibold">Sales Contract</a> 
                    <a href="#" class="dropdown-item d-item-gas font-size-12 font-semibold">Exports</a> 
                    <a href="#" class="dropdown-item d-item-gas font-size-12 font-semibold">DR/LS</a>
                    <a href="/sales-invoice/" class="dropdown-item d-item-gas font-size-12 font-semibold">Invoice</a> 
                </div>
            </div>
            <div class="btn-group mx-3">
                <a id="nav-purchase" href="#" class="" data-toggle="dropdown">Purchase</a>
                <div class="dropdown-menu b-radius-5 py-0">
                    <a href="/purchase-request/" class="dropdown-item d-item-gas font-size-12 font-semibold">Purchase Request</a>
                    <a href="/purchase-order/" class="dropdown-item d-item-gas font-size-12 font-semibold">Purchase Order</a>
                    <a href="/receiving-report/" class="dropdown-item d-item-gas font-size-12 font-semibold">Receiving Report</a>
                    <a href="/inward-inventory/" class="dropdown-item d-item-gas font-size-12 font-semibold">Inward Inventory</a> 
                    <a href="#" class="dropdown-item d-item-gas font-size-12 font-semibold">Completion Report</a> 
                    <a href="/payment-voucher/" class="dropdown-item d-item-gas font-size-12 font-semibold">Vouchers</a>
                </div>
            </div>
            <a href="/ledger/" class="mx-3" id="nav-reports">Reports</a>
            <a href="/customers/" class="mx-3" id="nav-customers">Customers</a>
            <a href="/vendors/" class="mx-3" id="nav-vendors">Vendors</a>
            <a href="#" class="mx-3" id="nav-bank-recon">Bank Reconciliation</a>
            <a href="/chart-of-accounts/" class="mx-3" id="nav-accounts">Chart of Accounts</a>
            <a href="#" class="mx-3" id="nav-ppe">PPE</a>
            <div class="btn-group mx-3">
                <a href="#" data-toggle="dropdown" id="nav-approvals">Approvals</a>
                <div class="dropdown-menu b-radius-5 py-0">
                    <a href="/pr-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Purchase Request</a>
                    <a href="/po-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Purchase Order</a>
                    <a href="/rr-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Receiving Report</a>
                    <a href="/ii-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Inward Inventory</a>
                    <div class="dropdown-divider"></div>
                    <a href="/qq-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Quotations</a>
                    <a href="/so-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Sales Order</a>
                    <a href="/sc-nonapproved/" class="dropdown-item d-item-gas font-size-12 font-semibold">Sales Contract</a>
                </div>
            </div>
        </div>

        <!-- Nav Controls -->
        <div class="c-nav-item justify-content-end align-items-center">
            <div class="icon-selector mx-3" onclick="toggleAppCard()">
                <img :src="this.const.iconSelector" alt="" height="20" id="appToggler">
            </div>
            <div class="notification mx-3">
                <img :src="this.const.bellIcon" alt="" height="20" class="notification-bell" id="notificationToggler">
            </div>
            <div class="profile mx-3" onclick="toggleProfile()">
                <img :src="this.photo" alt="" height="20" class="profile-border b-radius-circle" id="profileToggler">
            </div>
        </div>
    </div>
    `
})