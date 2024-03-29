Vue.component('navbar-pps', {
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
                ppsLogo: '/static/media/icons/PPS.svg',
                dashboardLogo: '/static/media/icons/Dashboard.svg',
                hrefProfile: '/static/media/icons/person.png'
            }
        }
    },
    mounted(){
        var x = document.getElementById(this.active);
        x.classList.add('active-pps');
    },

    template: /*javascript*/`
    <div class="c-nav d-flex mb-3 font-bold sticky-top" id="main-nav">
        <!-- LOGO CONTAINER -->
        <div class="c-nav-item justify-content-start">
            <img :src="this.const.ppsLogo" class="logo">
        </div>

        <!-- TABS CONTAINER -->
        <div class="pps-nav justify-content-center font-semibold navbar">
            <a href="/pps-planner/" class="mx-3" id="nav-planner">Project Planner</a>
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