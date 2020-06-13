from typing import Dict

from itypes.functions import FunctionType
from .print import Print

builtin_functions: Dict[str, FunctionType] = {
    "print": Print(),
}
