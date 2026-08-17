from _typeshed import Incomplete
from plyer.facades import Compass as Compass

class IosCompass(Compass):
    bridge: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
