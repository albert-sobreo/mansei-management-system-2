from ..models import *

def notify(request, title, subject, url, authLevel, *user):
    if user:
        for u in user:
            noti = Notifications()
            noti.user = u
            noti.title = title
            noti.subject = subject
            noti.url = url
            noti.authLevel = authLevel
            noti.save()
            request.user.branch.notifications.add(noti)
        return

    for branchUser in request.user.branch.user.all():
        print(int(branchUser.authLevel), authLevel, branchUser, request.user)
        if int(branchUser.authLevel) <= authLevel and branchUser != request.user:
            noti = Notifications()
            noti.user = branchUser
            noti.title = title
            noti.subject = subject
            noti.url = url
            noti.authLevel = authLevel
            noti.save()
            request.user.branch.notifications.add(noti)
    return