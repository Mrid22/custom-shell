from _typeshed import Incomplete
from plyer.facades import Gyroscope as Gyroscope

UIDevice: Incomplete
device: Incomplete

class IosGyroscope(Gyroscope):
    bridge: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
