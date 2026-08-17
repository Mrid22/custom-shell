from _typeshed import Incomplete
from plyer.facades import FileChooser as FileChooser

class Win32FileChooser:
    path: Incomplete
    multiple: bool
    filters: Incomplete
    preview: bool
    title: Incomplete
    icon: Incomplete
    show_hidden: bool
    def __init__(self, *args, **kwargs) -> None: ...
    selection: Incomplete
    def run(self): ...

class WinFileChooser(FileChooser): ...

def instance(): ...
