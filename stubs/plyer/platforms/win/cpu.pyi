from _typeshed import Incomplete
from ctypes import Structure, Union
from plyer.facades import CPU as CPU

KERNEL: Incomplete
ERROR_INSUFFICIENT_BUFFER: int

class CacheType:
    unified: int
    instruction: int
    data: int
    trace: int

class RelationshipType:
    processor_core: int
    numa_node: int
    cache: int
    processor_package: int
    group: int
    all: int

class CacheDescriptor(Structure): ...
class ProcessorCore(Structure): ...
class NumaNode(Structure): ...
class SystemLPIUnion(Union): ...
class SystemLPI(Structure): ...
class WinCPU(CPU): ...

def instance(): ...
