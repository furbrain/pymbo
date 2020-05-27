__add__(self, value) -> list
  Return self+value.

__class__ = type

__contains__(self, key) -> bool
  Return key in self.

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


__iadd__(self, value) -> list
  Implement self+=value.

__imul__(self, value) -> list
  Implement self*=value.

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

__mul__(self, value) -> list
  Return self*value.n

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> list
  Create and return a new object.  See help(type) for accurate signature.

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__reversed__() -> list
  L.__reversed__() -- return a reverse iterator over the list

__rmul__(self, value) -> list
  Return self*value.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__setitem__(self, key, value) -> None
  Set self[key] to value.

__sizeof__() -> int
  L.__sizeof__() -- size of L in memory, in bytes

__str__(self) -> str
  Return str(self).

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

append(object) -> None
  L.append(object) -> None -- append object to end

clear() -> None
  L.clear() -> None -- remove all items from L

copy() -> list
  L.copy() -> list -- a shallow copy of L

count(value) -> int
  L.count(value) -> integer -- return number of occurrences of value

extend(iterable) -> None
  L.extend(iterable) -> None -- extend list by appending elements from the iterable

index(value, start, stop) -> int
  L.index(value, [start, [stop]]) -> integer -- return first index of value.
  Raises ValueError if the value is not present.

insert() -> None
  L.insert(index, object) -- insert object before index

pop(index) -> Unknown
  L.pop([index]) -> item
  Raises IndexError if list is empty or index is out of range.

remove(value) -> None
  L.remove(value) -> None -- remove first occurrence of value.
  Raises ValueError if the value is not present.

reverse() -> None
  L.reverse() -- reverse *IN PLACE*

sort(key, reverse) -> None
  L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*

