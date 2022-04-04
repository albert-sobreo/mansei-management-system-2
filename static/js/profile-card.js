Vue.component('profile-card', {
    delimiters: ['[[', ']]'],
    props: [
        'first_name',
        'last_name',
        'position',
        'auth_level',
        'photo',
        'branch'
    ],

    template: /*javascript*/`
    <div class="profile-card b-radius-15 box-shadow-medium p-2 border" id="profileCard" style="display: none; z-index:1; width: 175px">
        <div class="flex flex-column profile-card-container py-2 px-4 b-radius-5 justify-content-center align-items-center">
            <div class="mb-2">
                <img class="profile-border b-radius-circle" :src="photo" alt="" height="40" width="40" style="object-fit:cover">
            </div>
            <div class="profile-my-name mt-1 text-center">
                <span class="font-semibold">[[this.first_name]]  [[this.last_name]]</span>
            </div>
            <div>
                <span>[[this.branch]]</span>
            </div>
            <div class="profile-my-position">
                <span>[[this.position]]</span>
            </div>
        </div>
        <div class="mt-2 flex flex-row profile-card-container logout py-2 px-4 b-radius-5 justify-content-center align-items-center " onclick="location.href='/my-profile/'">
            My Profile
        </div>
        <div class="mt-2 flex flex-row profile-card-container logout py-2 px-4 b-radius-5 justify-content-center align-items-center " onclick="location.href='/branches/'">
            Branch Settings
        </div>
        <div class="mt-2 flex flex-row profile-card-container logout py-2 px-4 b-radius-5 justify-content-center align-items-center " onclick="location.href='/logout/'">
            <i class="fas fa-sign-out-alt" style="color:#696969"></i><span>&nbsp;Logout</span>
        </div>
    </div>
    `
})