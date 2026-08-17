from _typeshed import Incomplete
from plyer.facades import Accelerometer as Accelerometer

class IosAccelerometer(Accelerometer):
    bridge: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
