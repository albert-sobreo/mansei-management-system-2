Vue.component('navbar-imps', {
    delimiters: ['[[', ']]'],
    props: [
        'active',
        'photo'
    ],
    data(){
        return{

            const: {
                iconSelector: '/static/media/icons/iconselector.svg',
                bellIcon: '/static/media/icons/bell-solid 1.svg',
                gasLogo: '/static/media/icons/GAS.svg',
                impsLogo: '/static/media/icons/imps.svg',
                emsLogo: '/static/media/icons/EMS.svg',
                dashboardLogo: '/static/media/icons/Dashboard.svg',
                hrefProfile: '/static/media/icons/person.png'
            },

            notiCount: 0
        }
    },

    mounted(){
        var x = document.getElementById(this.active);
        x.classList.add('active-imps');
        this.checkUnreadNoti()
        setInterval(this.checkUnreadNoti, 30000)
        
    },

    methods: {
        checkUnreadNoti(){
            axios.get('/notification-unread-checker/')
            .then(res=>this.notiCount=res.data)
        }
    },

    template: /*javascript*/`
    <div class="c-nav d-flex mb-3 font-bold" id="main-nav">
        <!-- LOGO CONTAINER -->
        <div class="c-nav-item justify-content-start">
            <img :src='this.const.impsLogo' class="logo">
        </div>

        <!-- TABS CONTAINER -->
        <div class="imps-nav justify-content-center font-semibold navbar">
            <a href='/merchinventory/' class="mx-3" id="nav-inventory">Inventory</a>
            <a href="/job-order/" class="mx-3" id="nav-job-order">Job Order</a>
            <a href="/transfer/" class="mx-3" id="nav-transfer">Transfer</a>
            <a href="/adjustments/" class="mx-3" id="nav-adjustments">Adjustments</a>
            <a href="/deliveries/" class="mx-3" id="nav-deliveries">Deliveries</a>
            <a href="/warehouse/" class="mx-3" id="nav-warehouse">Warehouse</a>
            <a href="#" class="mx-3" id="nav-reports">Reports</a>
            <div class="btn-group mx-3">
                <a id="nav-approvals" href="#" data-toggle="dropdown">Approvals</a>
                <div class="dropdown-menu b-radius-5 py-0">
                    <a href="/job-order-nonapproved/" class="dropdown-item d-item-imps font-size-12 font-semibold">Job Orders</a>
                    <a href="/tr-nonapproved/" class="dropdown-item d-item-imps font-size-12 font-semibold">Transfers</a>
                    <a href="/ad-nonapproved/" class="dropdown-item d-item-imps font-size-12 font-semibold">Adjustments</a>
                    <a href="/deliveriesnonapproved/" class="dropdown-item d-item-imps font-size-12 font-semibold">Deliveries</a>
                </div>
            </div>
        </div>

        <!-- NAV CONTROLS -->
        <div class="c-nav-item justify-content-end align-items-center">
            <div class="icon-selector mx-3" onclick="toggleAppCard()">
                <img :src="this.const.iconSelector" alt="" height="20" id="appToggler">
            </div>
            <div class="notification mx-3 position-relative" onclick="toggleNotificationCard()">
                <div v-if="notiCount" class="notification-number position-absolute" style="top:0px;right:0px"></div>
                <img :src="this.const.bellIcon" alt="" height="20" class="notification-bell" id="notificationToggler">
            </div>
            <div class="profile mx-3" onclick="toggleProfile()">
            <img :src="this.photo" alt="" height="20" width="20" class="profile-border b-radius-circle" id="profileToggler" style="object-fit:cover;">
            </div>
        </div>
    </div>
    `
})