from plyer.facades import Screenshot as Screenshot
from plyer.platforms.win.storagepath import WinStoragePath as WinStoragePath

class WinScreenshot(Screenshot):
    def __init__(self, file_path=None) -> None: ...

def instance(): ...
