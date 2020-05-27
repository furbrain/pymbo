__class__ = type

__contains__(self, key) -> bool
  Return key in self.

__delattr__(self, name) -> None
  Implement delattr(self, name).

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

__getitem__(self, key) -> int
  Return self[key].

__gt__(self, value) -> bool
  Return self>value.

__hash__(self) -> int
  Return hash(self).

__init__(self) -> None
  Initialize self.  See help(type(self)) for accurate signature.

__iter__(self) -> [int]
  Implement iter(self).

__le__(self, value) -> bool
  Return self<=value.

__len__(self) -> int
  Return len(self).

__lt__(self, value) -> bool
  Return self<value.

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> range
  Create and return a new object.  See help(type) for accurate signature.

__reduce__() -> Unknown

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__reversed__() -> [int]
  Return a reverse iterator.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  __sizeof__() -> int
  size of object in memory, in bytes

__str__(self) -> str
  Return str(self).

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

count() -> int
  rangeobject.count(value) -> integer -- return number of occurrences of value

index() -> int
  rangeobject.index(value, [start, [stop]]) -> integer -- return index of value.
  Raise ValueError if the value is not present.

start = int

step = int

stop = int

