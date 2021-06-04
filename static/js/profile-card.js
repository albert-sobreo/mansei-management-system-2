Vue.component('profile-card', {
    delimiters: ['[[', ']]'],
    props: [
        'first_name',
        'last_name',
        'position',
        'auth_level',
        'photo',
    ],

    template: /*javascript*/`
    <div class="profile-card b-radius-15 box-shadow-medium p-2 border" id="profileCard" style="display: none; z-index:1">
        <div class="flex flex-column profile-card-container py-2 px-4 b-radius-5 justify-content-center align-items-center border">
            <div class="mb-2">
                <img class="profile-border b-radius-circle" :src="photo" alt="" height="40" width="40">
            </div>
            <div class="profile-my-name mt-1">
                <span>[[this.first_name]]  [[this.last_name]]</span>
            </div>
            <div class="profile-my-position">
                <span>[[this.position]]</span>
            </div>
        </div>
        <div class="mt-2 flex flex-column profile-card-container logout py-2 px-4 b-radius-5 justify-content-center align-items-center border" onclick="location.href='/logout/'">
            Logout
        </div>
    </div>
    `
})