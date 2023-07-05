from __future__ import annotations
from typing import List, Dict, Union
MemoryValue = Union[str, int, float]
MemoryCore = Dict[str, Union[MemoryValue, List[MemoryValue], Dict[str, MemoryValue]]]
Memory = Dict[str, MemoryCore]

