import typing


class _PymboType:
    def __init__(self, real_type):
        self.real_type = real_type

    def __getitem__(self, params):
        if not isinstance(params, Tuple):
            params = (params,)
        new_params = []
        for p in params:
            if isinstance(p, slice):
                new_params.append(p.start)
            else:
                new_params.append(p)
        return self.real_type[tuple(new_params)]


List = _PymboType(typing.List)
Dict = _PymboType(typing.Dict)

Tuple = typing.Tuple

Int8 = int
Int16 = int
Int32 = int
Int64 = int

UInt8 = int
UInt16 = int
UInt32 = int
UInt64 = int
