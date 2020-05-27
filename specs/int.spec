__abs__(self) -> int
  abs(self)

__add__(self, value) -> int
  Return self+value.

__and__(self, value) -> int
  Return self&value.

__bool__(self) -> bool
  self != 0

__ceil__() -> int
  Ceiling of an Integral returns itself.

__class__ = type

__delattr__(self, name) -> None
  Implement delattr(self, name).

__dir__() -> [str]
  __dir__() -> list
  default dir() implementation

__divmod__(self, value) -> (int, int)
  Return divmod(self, value).

__doc__ = str

__eq__(self, value) -> bool
  Return self==value.

__float__(self) -> float
  float(self)

__floor__() -> int
  Flooring an Integral returns itself.

__floordiv__(self, value) -> int
  Return self//value.

__format__() -> str

__ge__(self, value) -> bool
  Return self>=value.

__getattribute__(self, name) -> Unknown
  Return getattr(self, name).

__getnewargs__() -> Unknown

__gt__(self, value) -> bool
  Return self>value.

__hash__(self) -> int
  Return hash(self).

__index__(self) -> int
  Return self converted to an integer, if self is suitable for use as an index into a list.

__init__(self) -> None
  Initialize self.  See help(type(self)) for accurate signature.

__int__(self) -> int
  int(self)

__invert__(self) -> int
  ~self

__le__(self, value) -> bool
  Return self<=value.

__lshift__(self, value) -> int
  Return self<<value.

__lt__(self, value) -> bool
  Return self<value.

__mod__(self, value) -> int
  Return self%value.

__mul__(self, value) -> int
  Return self*value.

__ne__(self, value) -> bool
  Return self!=value.

__neg__(self) -> int
  -self

__new__(type) -> int
  Create and return a new object.  See help(type) for accurate signature.

__or__(self, value) -> int
  Return self|value.

__pos__(self) -> int
  +self

__pow__(self, value, mod) -> int
  Return pow(self, value, mod).

__radd__(self, value) -> int
  Return value+self.

__rand__(self, value) -> int
  Return value&self.

__rdivmod__(self, value) -> (int, int)
  Return divmod(value, self).

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__rfloordiv__(self, value) -> int
  Return value//self.

__rlshift__(self, value) -> int
  Return value<<self.

__rmod__(self, value) -> int
  Return value%self.

__rmul__(self, value) -> int
  Return value*self.

__ror__(self, value) -> int
  Return value|self.

__round__() -> int
  Rounding an Integral returns itself.
  Rounding with an ndigits argument also returns an integer.

__rpow__(self, value, mod) -> int
  Return pow(value, self, mod).

__rrshift__(self, value) -> int
  Return value>>self.

__rshift__(self, value) -> int
  Return self>>value.

__rsub__(self, value) -> int
  Return value-self.

__rtruediv__(self, value) -> float
  Return value/self.

__rxor__(self, value) -> int
  Return value^self.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  Returns size in memory, in bytes

__str__(self) -> str
  Return str(self).

__sub__(self, value) -> int
  Return self-value.

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

__truediv__(self, value) -> float
  Return self/value.

__trunc__() -> Unknown
  Truncating an Integral returns itself.

__xor__(self, value) -> int
  Return self^value.

bit_length() -> int
  int.bit_length() -> int
  
  Number of bits necessary to represent self in binary.
  >>> bin(37)
  '0b100101'
  >>> (37).bit_length()
  6

conjugate() -> int
  Returns self, the complex conjugate of any int.

denominator = int
  the denominator of a rational number in lowest terms

from_bytes() -> int
  int.from_bytes(bytes, byteorder, *, signed=False) -> int
  
  Return the integer represented by the given array of bytes.
  
  The bytes argument must be a bytes-like object (e.g. bytes or bytearray).
  
  The byteorder argument determines the byte order used to represent the
  integer.  If byteorder is 'big', the most significant byte is at the
  beginning of the byte array.  If byteorder is 'little', the most
  significant byte is at the end of the byte array.  To request the native
  byte order of the host system, use `sys.byteorder' as the byte order value.
  
  The signed keyword-only argument indicates whether two's complement is
  used to represent the integer.

imag = int
  the imaginary part of a complex number

numerator = int
  the numerator of a rational number in lowest terms

real = int
  the real part of a complex number

to_bytes() -> bytes
  int.to_bytes(length, byteorder, *, signed=False) -> bytes
  
  Return an array of bytes representing an integer.
  
  The integer is represented using length bytes.  An OverflowError is
  raised if the integer is not representable with the given number of
  bytes.
  
  The byteorder argument determines the byte order used to represent the
  integer.  If byteorder is 'big', the most significant byte is at the
  beginning of the byte array.  If byteorder is 'little', the most
  significant byte is at the end of the byte array.  To request the native
  byte order of the host system, use `sys.byteorder' as the byte order value.
  
  The signed keyword-only argument determines whether two's complement is
  used to represent the integer.  If signed is False and a negative integer
  is given, an OverflowError is raised.

