__class__ = type

__contains__(self, key) -> bool
  True if D has a key k, else False.

__delattr__(self, name) -> None
  Implement delattr(self, name).

__delitem__(self, key) -> None
  Delete self[key].

__dir__() -> [str]
  __dir__() -> list
  default dir() implementation

__doc__ = str

__eq__(self, value) -> bool
  Return self==value.

__format__() -> str
  default object formatter

__ge__(self, value) -> bool
  Return self>=value.

__getattribute__(self, name) -> Unknown
  Return getattr(self, name).

__getitem__() -> Unknown
  x.__getitem__(y) <==> x[y]

__gt__(self, value) -> bool
  Return self>value.

__hash__ = None

__init__(self) -> None
  Initialize self.  See help(type(self)) for accurate signature.

__iter__(self) -> Unknown
  Implement iter(self).

__le__(self, value) -> bool
  Return self<=value.

__len__(self) -> int
  Return len(self).

__lt__(self, value) -> bool
  Return self<value.

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> dict
  Create and return a new object.  See help(type) for accurate signature.

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__setitem__(self, key, value) -> None
  Set self[key] to value.

__sizeof__() -> int
  D.__sizeof__() -> size of D in memory, in bytes

__str__(self) -> str
  Return str(self).

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

clear() -> None
  D.clear() -> None.  Remove all items from D.

copy() -> dict
  D.copy() -> a shallow copy of D

fromkeys(type, iterable, value) -> dict
  Returns a new dict with keys from iterable and values equal to value.

get(k, d) -> Unknown
  D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.

items() -> [Unknown]
  D.items() -> a set-like object providing a view on D's items

keys() -> [Unknown]
  D.keys() -> a set-like object providing a view on D's keys

pop(k, d) -> Unknown
  D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
  If key is not found, d is returned if given, otherwise KeyError is raised

popitem() -> (Unknown, Unknown)
  D.popitem() -> (k, v), remove and return some (key, value) pair as a
  2-tuple; but raise KeyError if D is empty.

setdefault(k, d) -> Unknown
  D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D

update(E, **F) -> None
  D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
  If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
  If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
  In either case, this is followed by: for k in F:  D[k] = F[k]

values() -> [Unknown]
  D.values() -> an object providing a view on D's values

