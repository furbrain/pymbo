__and__(self, value) -> frozenset
  Return self&value.

__class__ = type

__contains__() -> bool
  x.__contains__(y) <==> y in x.

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

__gt__(self, value) -> bool
  Return self>value.

__hash__(self) -> int
  Return hash(self).

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

__new__(type) -> frozenset
  Create and return a new object.  See help(type) for accurate signature.

__or__(self, value) -> frozenset
  Return self|value.

__rand__(self, value) -> frozenset
  Return value&self.

__reduce__() -> Unknown
  Return state information for pickling.

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__ror__(self, value) -> frozenset
  Return value|self.

__rsub__(self, value) -> frozenset
  Return value-self.

__rxor__(self, value) -> frozenset
  Return value^self.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  S.__sizeof__() -> size of S in memory, in bytes

__str__(self) -> str
  Return str(self).

__sub__(self, value) -> frozenset
  Return self-value.

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

__xor__(self, value) -> frozenset
  Return self^value.

copy() -> frozenset
  Return a shallow copy of a set.

difference(other) -> frozenset
  Return the difference of two or more sets as a new set.
  
  (i.e. all elements that are in this set but not the others.)

intersection(other) -> frozenset
  Return the intersection of two sets as a new set.
  
  (i.e. all elements that are in both sets.)

isdisjoint(other) -> bool
  Return True if two sets have a null intersection.

issubset(other) -> bool
  Report whether another set contains this set.

issuperset(other) -> bool
  Report whether this set contains another set.

symmetric_difference(other) -> frozenset
  Return the symmetric difference of two sets as a new set.
  
  (i.e. all elements that are in exactly one of the sets.)

union() -> frozenset
  Return the union of sets as a new set.
  
  (i.e. all elements that are in either set.)

