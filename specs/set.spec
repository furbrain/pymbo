__and__(self, value) -> set
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


__iand__(self, value) -> set
  Return self&=value.

__init__(self) -> None
  Initialize self.  See help(type(self)) for accurate signature.

__ior__(self, value) -> set
  Return self|=value.

__isub__(self, value) -> set
  Return self-=value.

__iter__(self) -> Unknown
  Implement iter(self).

__ixor__(self, value) -> set
  Return self^=value.

__le__(self, value) -> bool
  Return self<=value.

__len__(self) -> int
  Return len(self).

__lt__(self, value) -> bool
  Return self<value.

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> set
  Create and return a new object.  See help(type) for accurate signature.

__or__(self, value) -> set
  Return self|value.

__rand__(self, value) -> set
  Return value&self.

__reduce__() -> Unknown
  Return state information for pickling.

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__ror__(self, value) -> set
  Return value|self.

__rsub__(self, value) -> set
  Return value-self.

__rxor__(self, value) -> set
  Return value^self.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  S.__sizeof__() -> size of S in memory, in bytes

__str__(self) -> str
  Return str(self).

__sub__(self, value) -> set
  Return self-value.

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

__xor__(self, value) -> Unknown
  Return self^value.

add(item) -> None
  Add an element to a set.
  
  This has no effect if the element is already present.

clear() -> None
  Remove all elements from this set.

copy() -> set
  Return a shallow copy of a set.

difference(other) -> set
  Return the difference of two or more sets as a new set.
  
  (i.e. all elements that are in this set but not the others.)

difference_update(other) -> None
  Remove all elements of another set from this set.

discard(item) -> None
  Remove an element from a set if it is a member.
  
  If the element is not a member, do nothing.

intersection(other) -> set
  Return the intersection of two sets as a new set.
  
  (i.e. all elements that are in both sets.)

intersection_update(other) -> None
  Update a set with the intersection of itself and another.

isdisjoint(other) -> bool
  Return True if two sets have a null intersection.

issubset(other) -> bool
  Report whether another set contains this set.

issuperset(other) -> bool
  Report whether this set contains another set.

pop() -> Unknown
  Remove and return an arbitrary set element.
  Raises KeyError if the set is empty.

remove(item) -> None
  Remove an element from a set; it must be a member.
  
  If the element is not a member, raise a KeyError.

symmetric_difference(other) -> set
  Return the symmetric difference of two sets as a new set.
  
  (i.e. all elements that are in exactly one of the sets.)

symmetric_difference_update(other) -> None
  Update a set with the symmetric difference of itself and another.

union(other) -> set
  Return the union of sets as a new set.
  
  (i.e. all elements that are in either set.)

update(other) -> None
  Update a set with the union of itself and others.

