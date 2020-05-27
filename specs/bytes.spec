__add__(self, value) -> bytes
  Return self+value.

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

__getnewargs__() -> Unknown

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

__mod__(self, value) -> bytes
  Return self%value.

__mul__(self, value) -> bytes
  Return self*value.n

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> bytes
  Create and return a new object.  See help(type) for accurate signature.

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__rmod__(self, value) -> bytes
  Return value%self.

__rmul__(self, value) -> bytes
  Return self*value.

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

capitalize() -> bytes
  B.capitalize() -> copy of B
  
  Return a copy of B with only its first character capitalized (ASCII)
  and the rest lower-cased.

center(width, fillchar) -> bytes
  B.center(width[, fillchar]) -> copy of B
  
  Return B centered in a string of length width.  Padding is
  done using the specified fill character (default is a space).

count(sub, start, end) -> int
  B.count(sub[, start[, end]]) -> int
  
  Return the number of non-overlapping occurrences of substring sub in
  string B[start:end].  Optional arguments start and end are interpreted
  as in slice notation.

decode(self, encoding, errors) -> str
  Decode the bytes using the codec registered for encoding.
  
    encoding
      The encoding with which to decode the bytes.
    errors
      The error handling scheme to use for the handling of decoding errors.
      The default is 'strict' meaning that decoding errors raise a
      UnicodeDecodeError. Other possible values are 'ignore' and 'replace'
      as well as any other name registered with codecs.register_error that
      can handle UnicodeDecodeErrors.

endswith(suffix, start, end) -> bool
  B.endswith(suffix[, start[, end]]) -> bool
  
  Return True if B ends with the specified suffix, False otherwise.
  With optional start, test B beginning at that position.
  With optional end, stop comparing B at that position.
  suffix can also be a tuple of bytes to try.

expandtabs(tabsize) -> bytes
  B.expandtabs(tabsize=8) -> copy of B
  
  Return a copy of B where all tab characters are expanded using spaces.
  If tabsize is not given, a tab size of 8 characters is assumed.

find(sub, start, end) -> int
  B.find(sub[, start[, end]]) -> int
  
  Return the lowest index in B where substring sub is found,
  such that sub is contained within B[start:end].  Optional
  arguments start and end are interpreted as in slice notation.
  
  Return -1 on failure.

fromhex(type, string) -> bytes
  Create a bytes object from a string of hexadecimal numbers.
  
  Spaces between two numbers are accepted.
  Example: bytes.fromhex('B9 01EF') -> b'\\xb9\\x01\\xef'.

hex() -> str
  B.hex() -> string
  
  Create a string of hexadecimal numbers from a bytes object.
  Example: b'\xb9\x01\xef'.hex() -> 'b901ef'.

index(sub, start, end) -> int
  B.index(sub[, start[, end]]) -> int
  
  Like B.find() but raise ValueError when the substring is not found.

isalnum() -> bool
  B.isalnum() -> bool
  
  Return True if all characters in B are alphanumeric
  and there is at least one character in B, False otherwise.

isalpha() -> bool
  B.isalpha() -> bool
  
  Return True if all characters in B are alphabetic
  and there is at least one character in B, False otherwise.

isdigit() -> bool
  B.isdigit() -> bool
  
  Return True if all characters in B are digits
  and there is at least one character in B, False otherwise.

islower() -> bool
  B.islower() -> bool
  
  Return True if all cased characters in B are lowercase and there is
  at least one cased character in B, False otherwise.

isspace() -> bool
  B.isspace() -> bool
  
  Return True if all characters in B are whitespace
  and there is at least one character in B, False otherwise.

istitle() -> bool
  B.istitle() -> bool
  
  Return True if B is a titlecased string and there is at least one
  character in B, i.e. uppercase characters may only follow uncased
  characters and lowercase characters only cased ones. Return False
  otherwise.

isupper() -> bool
  B.isupper() -> bool
  
  Return True if all cased characters in B are uppercase and there is
  at least one cased character in B, False otherwise.

join(self, iterable_of_bytes) -> bytes
  Concatenate any number of bytes objects.
  
  The bytes whose method is called is inserted in between each pair.
  
  The result is returned as a new bytes object.
  
  Example: b'.'.join([b'ab', b'pq', b'rs']) -> b'ab.pq.rs'.

ljust(width, fillchar) -> bytes
  B.ljust(width[, fillchar]) -> copy of B
  
  Return B left justified in a string of length width. Padding is
  done using the specified fill character (default is a space).

lower() -> bytes
  B.lower() -> copy of B
  
  Return a copy of B with all ASCII characters converted to lowercase.

lstrip(self, bytes) -> bytes
  Strip leading bytes contained in the argument.
  
  If the argument is omitted or None, strip leading  ASCII whitespace.

maketrans(frm, to) -> Unknown
  Return a translation table useable for the bytes or bytes translate method.
  
  The returned table will be one where each byte in frm is mapped to the byte at
  the same position in to.
  
  The bytes objects frm and to must be of the same length.

partition(self, sep) -> (bytes, bytes, bytes)
  Partition the bytes into three parts using the given separator.
  
  This will search for the separator sep in the bytes. If the separator is found,
  returns a 3-tuple containing the part before the separator, the separator
  itself, and the part after it.
  
  If the separator is not found, returns a 3-tuple containing the original bytes
  object and two empty bytes objects.

replace(self, old, new, count) -> bytes
  Return a copy with all occurrences of substring old replaced by new.
  
    count
      Maximum number of occurrences to replace.
      -1 (the default value) means replace all occurrences.
  
  If the optional argument count is given, only the first count occurrences are
  replaced.

rfind(sub, start, end) -> int
  B.rfind(sub[, start[, end]]) -> int
  
  Return the highest index in B where substring sub is found,
  such that sub is contained within B[start:end].  Optional
  arguments start and end are interpreted as in slice notation.
  
  Return -1 on failure.

rindex(sub, start, end) -> int
  B.rindex(sub[, start[, end]]) -> int
  
  Like B.rfind() but raise ValueError when the substring is not found.

rjust(width, fillchar) -> bytes
  B.rjust(width[, fillchar]) -> copy of B
  
  Return B right justified in a string of length width. Padding is
  done using the specified fill character (default is a space)

rpartition(self, sep) -> (bytes, bytes, bytes)
  Partition the bytes into three parts using the given separator.
  
  This will search for the separator sep in the bytes, starting and the end. If
  the separator is found, returns a 3-tuple containing the part before the
  separator, the separator itself, and the part after it.
  
  If the separator is not found, returns a 3-tuple containing two empty bytes
  objects and the original bytes object.

rsplit(self, sep, maxsplit) -> [bytes]
  Return a list of the sections in the bytes, using sep as the delimiter.
  
    sep
      The delimiter according which to split the bytes.
      None (the default value) means split on ASCII whitespace characters
      (space, tab, return, newline, formfeed, vertical tab).
    maxsplit
      Maximum number of splits to do.
      -1 (the default value) means no limit.
  
  Splitting is done starting at the end of the bytes and working to the front.

rstrip(self, bytes) -> bytes
  Strip trailing bytes contained in the argument.
  
  If the argument is omitted or None, strip trailing ASCII whitespace.

split(self, sep, maxsplit) -> [bytes]
  Return a list of the sections in the bytes, using sep as the delimiter.
  
    sep
      The delimiter according which to split the bytes.
      None (the default value) means split on ASCII whitespace characters
      (space, tab, return, newline, formfeed, vertical tab).
    maxsplit
      Maximum number of splits to do.
      -1 (the default value) means no limit.

splitlines(self, keepends) -> [bytes]
  Return a list of the lines in the bytes, breaking at line boundaries.
  
  Line breaks are not included in the resulting list unless keepends is given and
  true.

startswith(prefix, start, end) -> bool
  B.startswith(prefix[, start[, end]]) -> bool
  
  Return True if B starts with the specified prefix, False otherwise.
  With optional start, test B beginning at that position.
  With optional end, stop comparing B at that position.
  prefix can also be a tuple of bytes to try.

strip(self, bytes) -> bytes
  Strip leading and trailing bytes contained in the argument.
  
  If the argument is omitted or None, strip leading and trailing ASCII whitespace.

swapcase() -> bytes
  B.swapcase() -> copy of B
  
  Return a copy of B with uppercase ASCII characters converted
  to lowercase ASCII and vice versa.

title() -> bytes
  B.title() -> copy of B
  
  Return a titlecased version of B, i.e. ASCII words start with uppercase
  characters, all remaining cased characters have lowercase.

translate() -> bytes
  translate(table, [deletechars])
  Return a copy with each character mapped by the given translation table.
  
    table
      Translation table, which must be a bytes object of length 256.
  
  All characters occurring in the optional argument deletechars are removed.
  The remaining characters are mapped through the given translation table.

upper() -> bytes
  B.upper() -> copy of B
  
  Return a copy of B with all ASCII characters converted to uppercase.

zfill(width) -> bytes
  B.zfill(width) -> copy of B
  
  Pad a numeric string B with zeros on the left, to fill a field
  of the specified width.  B is never truncated.

