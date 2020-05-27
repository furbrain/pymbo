__abs__(self) -> float
  abs(self)

__add__(self, value) -> complex
  Return self+value.

__bool__(self) -> bool
  self != 0

__class__ = type

__delattr__(self, name) -> None
  Implement delattr(self, name).

__dir__() -> [str]
  __dir__() -> list
  default dir() implementation

__divmod__(self, value) -> Unknown
  Return divmod(self, value).

__doc__ = str

__eq__(self, value) -> bool
  Return self==value.

__float__(self) -> float
  float(self)

__floordiv__(self, value) -> complex
  Return self//value.

__format__() -> str
  complex.__format__() -> str
  
  Convert to a string according to format_spec.

__ge__(self, value) -> bool
  Return self>=value.

__getattribute__(self, name) -> Unknown
  Return getattr(self, name).

__getnewargs__() -> Unknown

__gt__(self, value) -> bool
  Return self>value.

__hash__(self) -> int
  Return hash(self).

__init__(self) -> None
  Initialize self.  See help(type(self)) for accurate signature.

__int__(self) -> int
  int(self)

__le__(self, value) -> bool
  Return self<=value.

__lt__(self, value) -> bool
  Return self<value.

__mod__(self, value) -> complex
  Return self%value.

__mul__(self, value) -> complex
  Return self*value.

__ne__(self, value) -> bool
  Return self!=value.

__neg__(self) -> complex
  -self

__new__(type) -> complex
  Create and return a new object.  See help(type) for accurate signature.

__pos__(self) -> complex
  +self

__pow__(self, value, mod) -> complex
  Return pow(self, value, mod).

__radd__(self, value) -> complex
  Return value+self.

__rdivmod__(self, value) -> Unknown
  Return divmod(value, self).

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__rfloordiv__(self, value) -> complex
  Return value//self.

__rmod__(self, value) -> complex
  Return value%self.

__rmul__(self, value) -> complex
  Return value*self.

__rpow__(self, value, mod) -> complex
  Return pow(value, self, mod).

__rsub__(self, value) -> complex
  Return value-self.

__rtruediv__(self, value) -> complex
  Return value/self.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  __sizeof__() -> int
  size of object in memory, in bytes

__str__(self) -> str
  Return str(self).

__sub__(self, value) -> complex
  Return self-value.

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

__truediv__(self, value) -> Unknown
  Return self/value.

conjugate() -> complex
  complex.conjugate() -> complex
  
  Return the complex conjugate of its argument. (3-4j).conjugate() == 3+4j.

imag = float
  the imaginary part of a complex number

real = float
  the real part of a complex number
