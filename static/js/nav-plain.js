Vue.component('navbar-plain', {
    delimiters: ['[[', ']]'],
    props: [
        'photo',
        'name'
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
            }
        }
    },

    template: /*javascript*/`
    <div class="c-nav d-flex mb-3 font-bold sticky-top" id="main-nav">
        <!-- LOGO CONTAINER -->
        <div class="c-nav-item justify-content-start">
            <span>[[name]]</span>
        </div>

        <!-- TABS CONTAINER -->
        <div class="imps-nav justify-content-center font-semibold navbar">
            
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