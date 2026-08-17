from plyer.facades import Screenshot as Screenshot
from plyer.platforms.linux.storagepath import LinuxStoragePath as LinuxStoragePath
from plyer.utils import whereis_exe as whereis_exe

class LinuxScreenshot(Screenshot):
    def __init__(self, file_path=None) -> None: ...

def instance(): ...
