from _typeshed import Incomplete
from plyer.facades import Brightness as Brightness

UIScreen: Incomplete

class iOSBrightness(Brightness):
    screen: Incomplete
    def __init__(self) -> None: ...
    def set_level(self, level) -> None: ...

def instance(): ...
