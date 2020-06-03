from itypes import InferredType
from typing import Optional, Sequence, Dict

from itypes.lister import Lister


class TypeDB:
    def __init__(self):
        self.types: Dict[str, InferredType] = {}

    def get_list(self, elements: Sequence[InferredType], maxlen: Optional[int] = None):
        if maxlen is None:
            maxlen = 40
        tp = Lister.from_elements(elements, maxlen)
        return self.types.setdefault(tp.as_c_type(), tp)

    def __iter__(self):
        return iter(self.types.values())
