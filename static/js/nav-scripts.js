//initialize Navbar Profile Card and App Card
var cards = {
    profileCard: document.getElementById('profileCard'),
    appCard: document.getElementById('appCard')
}
var proceed = true
cards.profileCard.onmousedown = () => {
    proceed = false
}
cards.appCard.onmousedown = () => {
    proceed = false
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
    if (!cards.profileCard.contains(event.target) || !cards.appCard.contains(event.target)){
        profileCard.style.display = 'none'
        appCard.style.display = 'none'
    }
})
//Toggles Profile Card
toggleProfile = () => {
    if (cards.profileCard.style.display == "none" || cards.appCard.style.display == 'block'){
        profileCard.style.display = 'block'
        appCard.style.display = 'none'
    } else {
        profileCard.style.display = 'none'
    }
}
//Toggles App Card
toggleAppCard = () => {
    if (cards.appCard.style.display == 'none' || cards.profileCard.style.display == 'block'){
        appCard.style.display = 'block'
        profileCard.style.display = 'none'
    } else {
        appCard.style.display = 'none'
    }
}