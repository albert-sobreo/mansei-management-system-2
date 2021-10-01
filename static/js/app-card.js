Vue.component('app-card', {
    delimiters: ['[[', ']]'],
    data(){
        return {
            const:{
                gasLogo: '/static/media/icons/GAS.svg',
                impsLogo: '/static/media/icons/imps.svg',
                emsLogo: '/static/media/icons/EMS.svg',
                dashboardLogo: '/static/media/icons/Dashboard.svg',
            }
        }
    },
    template: /*javascript*/`
    <div class="app-card b-radius-15 box-shadow-medium p-3 border" id="appCard" style="display: none; z-index:1">
        <div onclick="location.href='/'" class="flex flex-column app-card-links dashboard border align-items-center justify-content-center mb-2 py-3 px-4 b-radius-10">
            <img :src="this.const.dashboardLogo" alt="">
        </div>
        <div onclick="location.href='/merchinventory/'" class="flex flex-column app-card-links imps border align-items-center justify-content-center my-3 py-3 px-4 b-radius-10">
            <img :src="this.const.impsLogo" alt="">
        </div>
        <div onclick="location.href='/journal/'" class="flex flex-column app-card-links gas border align-items-center justify-content-center my-3 py-3 px-4 b-radius-10">
            <img :src="this.const.gasLogo" alt="">
        </div>
        <div onclick="location.href='/ems-my-dtr/'" class="flex flex-column app-card-links ems border align-items-center justify-content-center mt-3 py-3 px-4 b-radius-10">
            <img :src="this.const.emsLogo" alt="">
        </div>
    </div>
    `
})