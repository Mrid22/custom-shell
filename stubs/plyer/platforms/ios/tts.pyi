from _typeshed import Incomplete
from plyer.facades import TTS as TTS

AVSpeechUtterance: Incomplete
AVSpeechSynthesizer: Incomplete
AVSpeechSynthesisVoice: Incomplete

class iOSTextToSpeech(TTS):
    synth: Incomplete
    voice: Incomplete
    def __init__(self) -> None: ...

def instance(): ...
