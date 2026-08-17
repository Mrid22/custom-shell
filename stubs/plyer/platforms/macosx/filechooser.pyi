from _typeshed import Incomplete
from plyer.facades import FileChooser as FileChooser

NSURL: Incomplete
NSOpenPanel: Incomplete
NSSavePanel: Incomplete
NSOKButton: int

class MacFileChooser:
    mode: str
    path: Incomplete
    multiple: bool
    filters: Incomplete
    preview: bool
    title: Incomplete
    icon: Incomplete
    show_hidden: bool
    use_extensions: bool
    def __init__(self, *args, **kwargs) -> None: ...
    def run(self): ...

class MacOSXFileChooser(FileChooser): ...

def instance(): ...
