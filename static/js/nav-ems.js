Vue.component('navbar-ems', {
    delimiters: ['[[', ']]'],
    props: [
        'active'
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
            }
        }
    },
    mounted(){
        var x = document.getElementById(this.active);
        x.classList.add('active-ems');
    },

    template: /*javascript*/`
    <div class="c-nav d-flex mb-3 font-bold" id="main-nav">
        <!-- LOGO CONTAINER -->
        <div class="c-nav-item justify-content-start">
            <img :src="this.const.emsLogo" class="logo">
        </div>

        <!-- TABS CONTAINER -->
        <div class="ems-nav justify-content-center font-semibold navbar">
            <a href="#" class="mx-3" id="nav-dtr">DTR</a>
            <a href="#" class="mx-3" id="nav-timesheet">Timesheet</a>
            <a href="#" class="mx-3" id="nav-payslip">Payslip</a>
            <a href="#" class="mx-3" id="nav-requests">Requests</a>
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
                <img :src="this.const.hrefProfile" alt="" height="20" class="profile-border b-radius-circle" id="profileToggler">
            </div>
        </div>
    </div>
    `
})