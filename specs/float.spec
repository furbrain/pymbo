__abs__(self) -> float
  abs(self)

__add__(self, value) -> float
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

__floordiv__(self, value) -> float
  Return self//value.

__format__() -> str
  float.__format__(format_spec) -> string
  
  Formats the float according to format_spec.

__ge__(self, value) -> bool
  Return self>=value.

__getattribute__(self, name) -> Unknown
  Return getattr(self, name).

__getformat__() -> Unknown
  float.__getformat__(typestr) -> string
  
  You probably don't want to use this function.  It exists mainly to be
  used in Python's test suite.
  
  typestr must be 'double' or 'float'.  This function returns whichever of
  'unknown', 'IEEE, big-endian' or 'IEEE, little-endian' best describes the
  format of floating point numbers used by the C type named by typestr.

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

__mod__(self, value) -> float
  Return self%value.

__mul__(self, value) -> float
  Return self*value.

__ne__(self, value) -> bool
  Return self!=value.

__neg__(self) -> float
  -self

__new__(type) -> float
  Create and return a new object.  See help(type) for accurate signature.

__pos__(self) -> float
  +self

__pow__(self, value, mod) -> float
  Return pow(self, value, mod).

__radd__(self, value) -> float
  Return value+self.

__rdivmod__(self, value) -> float
  Return divmod(value, self).

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__rfloordiv__(self, value) -> float
  Return value//self.

__rmod__(self, value) -> float
  Return value%self.

__rmul__(self, value) -> float
  Return value*self.

__round__() -> int
  Return the Integral closest to x, rounding half toward even.
  When an argument is passed, work like built-in round(x, ndigits).

__rpow__(self, value, mod) -> float
  Return pow(value, self, mod).

__rsub__(self, value) -> float
  Return value-self.

__rtruediv__(self, value) -> float
  Return value/self.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__setformat__() -> None
  float.__setformat__(typestr, fmt) -> None
  
  You probably don't want to use this function.  It exists mainly to be
  used in Python's test suite.
  
  typestr must be 'double' or 'float'.  fmt must be one of 'unknown',
  'IEEE, big-endian' or 'IEEE, little-endian', and in addition can only be
  one of the latter two if it appears to match the underlying C reality.
  
  Override the automatic determination of C-level floating point type.
  This affects how floats are converted to and from binary strings.

__sizeof__() -> int
  __sizeof__() -> int
  size of object in memory, in bytes

__str__(self) -> str
  Return str(self).

__sub__(self, value) -> float
  Return self-value.

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

__truediv__(self, value) -> float  
  Return self/value.

__trunc__() -> int
  Return the Integral closest to x between 0 and x.

as_integer_ratio() -> (int, int)
  float.as_integer_ratio() -> (int, int)
  
  Return a pair of integers, whose ratio is exactly equal to the original
  float and with a positive denominator.
  Raise OverflowError on infinities and a ValueError on NaNs.
  
  >>> (10.0).as_integer_ratio()
  (10, 1)
  >>> (0.0).as_integer_ratio()
  (0, 1)
  >>> (-.25).as_integer_ratio()
  (-1, 4)

conjugate() -> float
  Return self, the complex conjugate of any float.

fromhex() -> float
  float.fromhex(string) -> float
  
  Create a floating-point number from a hexadecimal string.
  >>> float.fromhex('0x1.ffffp10')
  2047.984375
  >>> float.fromhex('-0x1p-1074')
  -5e-324

hex() -> str
  float.hex() -> string
  
  Return a hexadecimal representation of a floating-point number.
  >>> (-0.1).hex()
  '-0x1.999999999999ap-4'
  >>> 3.14159.hex()
  '0x1.921f9f01b866ep+1'

imag = float
  the imaginary part of a complex number

is_integer() -> bool
  Return True if the float is an integer.

real = float
  the real part of a complex number

