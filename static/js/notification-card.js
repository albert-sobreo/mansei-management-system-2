Vue.component('notification-card', {
    delimiters: ['[[', ']]'],
    data(){
        return {
            notifications: [{
                user: null,
                title: null,
                subject: null,
                url: null,
                read: null,
                authLevel: null,
                datetimeCreated: null
            }],

            config: {
                headers:{
                    "X-CSRFToken": getCookie('csrftoken')
                }
            },
        }
    },

    mounted(){
        this.fetchNoti()
        setInterval(this.fetchNoti, 30000)
    },

    methods: {
        onclick(id){
            axios.get(`/notifications/${id}/`)
            .then(res=>{
                location.href = res.data
            })
        },
        fetchNoti(){
            axios.get('/api/notifications/')
            .then(res=>{
                this.notifications = res.data
            })
        },
        deleteNoti(id){
            axios.delete(`/api/notifications/${id}/`, this.config)
            .then(res=>this.fetchNoti())
        },

        formatDateTime(value){
            const months = [
                'Jan',
                'Feb',
                'Mar',
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec'
            ]

            const days = [
                'Sun',
                'Mon',
                'Tue',
                'Wed',
                'Thu',
                'Fri',
                'Sat'
            ]

            value = new Date(value)
            year = value.getFullYear()
            month = months[value.getMonth()]
            date = value.getDate()
            hour = (value.getHours() + 24) % 12 || 12; 
            minute = (value.getMinutes()<10?'0':'') + value.getMinutes()
            day = days[value.getDay()]
            meridian = value.getHours() >= 12 ? 'pm' : 'am'
            formatted = `${month}. ${date}, ${year} - ${hour}:${minute} ${meridian}`

            return formatted
        },

        timeSince(date){
            return moment(date).fromNow(true)
        },
    },

    template: /*javascript*/`
    <div class="app-card b-radius-10 pb-2 box-shadow-medium px-3 border" id="notificationCard" style="display: none; z-index:1; width: 250px">
        <div class="row my-2">
            <div class="col">
                <span class="font-size-18 font-bold">Notifications</span>
            </div>
        </div>
        <div class="row my-2" v-for="item in notifications">
            <div class="col mx-2 pr-0 notification-item b-radius-5 box-shadow-small" v-if="item.read">
                <div class="d-flex justify-content-between">
                    <div class="my-1" v-on:click="onclick(item.id)">
                        <span class="font-bold soft-text">[[item.title]]</span><br>
                        <span class="font-regular softer-text">[[item.subject]]</span><br>
                    </div>
                    <div v-on:click="deleteNoti(item.id)" style="width:20px" class="notification-delete b-tr-radius-5 b-br-radius-5 d-flex justify-content-center align-items-center">
                        <span><i class="fas fa-trash-alt"></i></span>
                    </div>
                </div>
            </div>
            <div class="col mx-2 pr-0 notification-item b-radius-5 box-shadow-small notification-item-new" v-else>
                <div class="d-flex justify-content-between">
                    <div class="my-1" v-on:click="onclick(item.id)">
                        <span class="font-bold soft-text">[[item.title]]</span><br>
                        <span class="font-regular softer-text">[[item.subject]]</span><br>
                        <span class="font-regular softer-text font-size-10">[[timeSince(item.datetimeCreated)]]</span>
                    </div>
                    <div v-on:click="deleteNoti(item.id)" style="width:20px" class="notification-delete b-tr-radius-5 b-br-radius-5 d-flex justify-content-center align-items-center">
                        <span><i class="fas fa-trash-alt"></i></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
})