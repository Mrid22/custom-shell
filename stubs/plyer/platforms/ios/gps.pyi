from _typeshed import Incomplete
from plyer.facades import GPS as GPS

CLLocationManager: Incomplete

class IosGPS(GPS):
    def locationManager_didChangeAuthorizationStatus_(self, manager, status) -> None: ...
    def locationManager_didUpdateLocations_(self, manager, locations) -> None: ...

def instance(): ...
