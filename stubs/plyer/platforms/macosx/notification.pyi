from _typeshed import Incomplete
from plyer.facades import Notification as Notification

NSUserNotification: Incomplete
NSUserNotificationCenter: Incomplete

class OSXNotification(Notification):
    def userNotificationCenter_shouldPresentNotification_(self, center, notification): ...

def instance(): ...
