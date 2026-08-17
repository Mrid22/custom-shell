from _typeshed import Incomplete
from plyer.facades import Battery as Battery

UIDevice: Incomplete

class IOSBattery(Battery):
    device: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
