from plyer.facades import Screenshot as Screenshot
from plyer.platforms.macosx.storagepath import OSXStoragePath as OSXStoragePath
from plyer.utils import whereis_exe as whereis_exe

class OSXScreenshot(Screenshot):
    def __init__(self, file_path=None) -> None: ...

def instance(): ...
