from _typeshed import Incomplete
from plyer.facades import StoragePath as StoragePath

NSFileManager: Incomplete
NSApplicationDirectory: int
NSDocumentDirectory: int
NSDownloadsDirectory: int
NSMoviesDirectory: int
NSMusicDirectory: int
NSPicturesDirectory: int

class iOSStoragePath(StoragePath):
    defaultManager: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
