from typing import Dict

from itypes.functions import FixedFunctionType
from .print import Print

builtin_functions: Dict[str, FixedFunctionType] = {
    "print": Print(),
}
