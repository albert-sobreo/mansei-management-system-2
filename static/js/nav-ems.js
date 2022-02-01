Vue.component('navbar-ems', {
    delimiters: ['[[', ']]'],
    props: [
        'active',
        'photo'
    ],
    data(){
        return{
            user:{
                firstName: null,
                lastName: null,
                position: null,
                authLevel: null,
                photo: null,
            },

            const:{
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
        x.classList.add('active-ems');
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
            <img :src="this.const.emsLogo" class="logo">
        </div>

        <!-- TABS CONTAINER -->
        <div class="ems-nav justify-content-center font-semibold navbar">
            <a href="/ems-my-dtr/" class="mx-3" id="nav-dtr">DTR</a>
            <a href="/ems-my-timesheet/" class="mx-3" id="nav-timesheet">Timesheet</a>
            <a href="/ems-my-payslip/" class="mx-3" id="nav-payslip">Payslip</a>
            <a href="/ems-payroll/" class="mx-3" id="nav-payroll">Payroll</a>
            <a href="/ems-deduction-sss/" class="mx-3" id="nav-deductions">Deductions</a>
            <a href="/ems-loans-sss/" class="mx-3" id="nav-loans">Loans</a>
            <a href="/ems-employees/" class="mx-3" id="nav-employees">Employees</a>
            <a href="/ems-holidays/" class="mx-3" id="nav-holidays">Holidays</a>
            <a href="/ems-overtime-request/" class="mx-3" id="nav-requests">Requests</a>
            <div class="btn-group mx-3">
                <a href="#" data-toggle="dropdown" id="nav-approvals">Approvals</a>
                <div class="dropdown-menu b-radius-5 py-0">
                    <a href="/ems-overtime-pending/" class="dropdown-item d-item-ems font-size-12 font-semibold">Overtime</a>
                    <a href="/ems-undertime-pending/" class="dropdown-item d-item-ems font-size-12 font-semibold">Undertime</a>
                    <a href="/ems-leave-pending/" class="dropdown-item d-item-ems font-size-12 font-semibold">Leave</a>
                </div>
            </div>
        </div>

        <!-- NAV CONTROLS -->
        <div class="c-nav-item justify-content-end align-items-center">
        <div class="icon-selector mx-3" onclick="toggleAppCard()">
                <img :src="this.const.iconSelector" alt="" height="20" id="appToggler">
            </div>
            <div class="notification mx-3">
                <img :src="this.const.bellIcon" alt="" height="20" class="notification-bell" id="notificationToggler">
            </div>
            <div class="profile mx-3" onclick="toggleProfile()">
            <img :src="this.photo" alt="" height="20" width="20" class="profile-border b-radius-circle" id="profileToggler" style="object-fit:cover;">
            </div>
        </div>
    </div>
    `
})