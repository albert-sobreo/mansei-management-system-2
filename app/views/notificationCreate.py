from ..models import *

def notify(request, title, subject, url, authLevel):
    for branchUser in request.user.branch.user.all():
        if int(branchUser.authLevel) <= authLevel or branchUser != request.user:
            noti = Notifications()
            noti.user = branchUser
            noti.title = title
            noti.subject = subject
            noti.url = url
            noti.authLevel = authLevel
            noti.save()
            request.user.branch.notifications.add(noti)