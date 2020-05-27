__abstractmethods__ = Unknown

__base__ = type

__bases__ = tuple

__basicsize__ = int

__call__(self) -> Unknown
  Call self as a function.

__class__ = type

__delattr__(self, name) -> None
  Implement delattr(self, name).


__dictoffset__ = int

__dir__() -> [str]
  __dir__() -> list
  specialized __dir__ implementation for types

__doc__ = str

__eq__(self, value) -> bool
  Return self==value.

__flags__ = int

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

__instancecheck__() -> bool
  __instancecheck__() -> bool
  check if an object is an instance

__itemsize__ = int

__le__(self, value) -> bool
  Return self<=value.

__lt__(self, value) -> bool
  Return self<value.

__module__ = str

__mro__ = tuple

__name__ = str

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> type
  Create and return a new object.  See help(type) for accurate signature.

__prepare__() -> dict
  __prepare__() -> dict
  used to create the namespace for the class statement

__qualname__ = str

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  __sizeof__() -> int
  return memory consumption of the type object

__str__(self) -> str
  Return str(self).

__subclasscheck__() -> bool
  __subclasscheck__() -> bool
  check if a class is a subclass

__subclasses__() -> [type]
  __subclasses__() -> list of immediate subclasses

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

__text_signature__ = None

__weakrefoffset__ = int

mro() -> [type]
  mro() -> list
  return a type's method resolution order

