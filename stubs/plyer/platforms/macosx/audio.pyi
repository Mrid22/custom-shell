from _typeshed import Incomplete
from plyer.facades import Audio as Audio
from plyer.platforms.macosx.storagepath import OSXStoragePath as OSXStoragePath

AVAudioPlayer: Incomplete
AVAudioRecorder: Incomplete
AVAudioFormat: Incomplete
NSString: Incomplete
NSURL: Incomplete
NSError: Incomplete

class OSXAudio(Audio):
    def __init__(self, file_path=None) -> None: ...

def instance(): ...
