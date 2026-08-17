from _typeshed import Incomplete
from plyer.facades import Barometer as Barometer

class iOSBarometer(Barometer):
    bridge: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
