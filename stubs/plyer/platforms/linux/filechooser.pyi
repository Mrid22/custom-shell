from _typeshed import Incomplete
from plyer.facades import FileChooser as FileChooser

class SubprocessFileChooser:
    executable: str
    separator: str
    successretcode: int
    path: Incomplete
    multiple: bool
    filters: Incomplete
    preview: bool
    title: Incomplete
    icon: Incomplete
    show_hidden: bool
    def __init__(self, *args, **kwargs) -> None: ...
    def run(self): ...

class ZenityFileChooser(SubprocessFileChooser):
    executable: str
    separator: str
    successretcode: int

class KDialogFileChooser(SubprocessFileChooser):
    executable: str
    separator: str
    successretcode: int

class YADFileChooser(SubprocessFileChooser):
    executable: str
    separator: str
    successretcode: int

CHOOSERS: Incomplete

class LinuxFileChooser(FileChooser):
    desktop: Incomplete

def instance(): ...
