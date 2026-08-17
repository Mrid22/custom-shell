import ctypes
from _typeshed import Incomplete
from ctypes import Structure

ERROR_DICT: Incomplete
IOKit: Incomplete

class data_structure(Structure): ...

void_p: Incomplete
kern_return_t = ctypes.c_int
KERN_SUCCESS: int
KERN_FUNC: int
mach_port_t = void_p
MACH_PORT_NULL: int
io_object_t = ctypes.c_int
io_object_t = ctypes.c_int
io_iterator_t = void_p
io_object_t = void_p
io_connect_t = void_p
IOItemCount = ctypes.c_uint
CFMutableDictionaryRef = void_p

def is_os_64bit(): ...
def read_sms(): ...
def get_coord(): ...
