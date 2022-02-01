//initialize Navbar Profile Card and App Card
var cards = {
    profileCard: document.getElementById('profileCard'),
    appCard: document.getElementById('appCard'),
    notificationCard: document.getElementById('notificationCard')
}
var proceed = true
try{
    cards.profileCard.onmousedown = () => {
        proceed = false
    }
} catch(err){
    console.log(err)
}

try{
    cards.appCard.onmousedown = () => {
        proceed = false
    }
} catch(err){
    console.log(err)
}
try{
    cards.notificationCard.onmousedown = () => {
        proceed = false
    }
} catch(err){
    console.log(err)
}
//Add Event listener for mouseup
//Hide all cards on outside click
document.addEventListener('mouseup', function(event){
    if(event.target.id == 'appToggler' || event.target.id == 'notificationToggler' || event.target.id == 'profileToggler' ){
        return
    }
    if(!proceed){
        proceed = true
        return
    }
    if (!cards.profileCard.contains(event.target) || !cards.appCard.contains(event.target) || !cards.notificationCard.contains(event.target)){
        profileCard.style.display = 'none'
        appCard.style.display = 'none'
        notificationCard.style.display = 'none'
    }
})
//Toggles Profile Card
toggleProfile = () => {
    if (cards.profileCard.style.display == "none" || cards.notificationCard.style.display == 'block' || cards.appCard.style.display == 'block'){
        profileCard.style.display = 'block'
        appCard.style.display = 'none'
        notificationCard.style.display = 'none'
    } else {
        profileCard.style.display = 'none'
    }
}
//Toggles App Card
toggleAppCard = () => {
    if (cards.appCard.style.display == 'none' || cards.notificationCard.style.display == 'block' || cards.profileCard.style.display == 'block'){
        appCard.style.display = 'block'
        profileCard.style.display = 'none'
        notificationCard.style.display = 'none'
    } else {
        appCard.style.display = 'none'
    }
},

toggleNotificationCard = () => {
    if (cards.appCard.style.display == 'block' || cards.notificationCard.style.display == 'none' || cards.profileCard.style.display == 'block'){
        appCard.style.display = 'none'
        profileCard.style.display = 'none'
        notificationCard.style.display = 'block'
    } else {
        notificationCard.style.display = 'none'
    }
}