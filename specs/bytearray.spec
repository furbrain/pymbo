__add__(self, value) -> bytearray
  Return self+value.

__alloc__() -> int
  B.__alloc__() -> int
  
  Return the number of bytes actually allocated.

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

__getitem__(self, key) -> int
  Return self[key].

__gt__(self, value) -> bool
  Return self>value.

__iadd__(self, value) -> bytearray
  Implement self+=value.

__imul__(self, value) -> bytearray
  Implement self*=value.

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

__mod__(self, value) -> bytearray
  Return self%value.

__mul__(self, value) -> bytearray
  Return self*value.n

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> bytearray
  Create and return a new object.  See help(type) for accurate signature.

__reduce__(self) -> Unknown
  Return state information for pickling.

__reduce_ex__(self, proto) -> Unknown
  Return state information for pickling.

__repr__(self) -> str
  Return repr(self).

__rmod__(self, value) -> bytearray
  Return value%self.

__rmul__(self, value) -> bytearray
  Return self*value.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__setitem__(self, key, value) -> None
  Set self[key] to value.

__sizeof__(self) -> int
  Returns the size of the bytearray object in memory, in bytes.

__str__(self) -> str
  Return str(self).

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

append(self, item) -> None
  Append a single item to the end of the bytearray.
  
    item
      The item to be appended.

capitalize() -> bytearray
  B.capitalize() -> copy of B
  
  Return a copy of B with only its first character capitalized (ASCII)
  and the rest lower-cased.

center(width, fillchar) -> bytearray
  B.center(width[, fillchar]) -> copy of B
  
  Return B centered in a string of length width.  Padding is
  done using the specified fill character (default is a space).

clear(self) -> None
  Remove all items from the bytearray.

copy(self) -> bytearray
  Return a copy of B.

count(sub, start, end) -> int
  B.count(sub[, start[, end]]) -> int
  
  Return the number of non-overlapping occurrences of subsection sub in
  bytes B[start:end].  Optional arguments start and end are interpreted
  as in slice notation.

decode(self, encoding, errors) -> str
  Decode the bytearray using the codec registered for encoding.
  
    encoding
      The encoding with which to decode the bytearray.
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

expandtabs(tabsize) -> bytearray
  B.expandtabs(tabsize=8) -> copy of B
  
  Return a copy of B where all tab characters are expanded using spaces.
  If tabsize is not given, a tab size of 8 characters is assumed.

extend(self, iterable_of_ints) -> None
  Append all the items from the iterator or sequence to the end of the bytearray.
  
    iterable_of_ints
      The iterable of items to append.

find(sub, start, end) -> int
  B.find(sub[, start[, end]]) -> int
  
  Return the lowest index in B where subsection sub is found,
  such that sub is contained within B[start,end].  Optional
  arguments start and end are interpreted as in slice notation.
  
  Return -1 on failure.

fromhex(type, string) -> bytearray
  Create a bytearray object from a string of hexadecimal numbers.
  
  Spaces between two numbers are accepted.
  Example: bytearray.fromhex('B9 01EF') -> bytearray(b'\\xb9\\x01\\xef')

hex() -> str
  B.hex() -> string
  
  Create a string of hexadecimal numbers from a bytearray object.
  Example: bytearray([0xb9, 0x01, 0xef]).hex() -> 'b901ef'.

index(sub, start, end) -> int
  B.index(sub[, start[, end]]) -> int
  
  Like B.find() but raise ValueError when the subsection is not found.

insert(self, index, item) -> None
  Insert a single item into the bytearray before the given index.
  
    index
      The index where the value is to be inserted.
    item
      The item to be inserted.

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

join(self, iterable_of_bytes) -> bytearray
  Concatenate any number of bytes/bytearray objects.
  
  The bytearray whose method is called is inserted in between each pair.
  
  The result is returned as a new bytearray object.

ljust(width, fillchar) -> bytearray
  B.ljust(width[, fillchar]) -> copy of B
  
  Return B left justified in a string of length width. Padding is
  done using the specified fill character (default is a space).

lower() -> bytearray
  B.lower() -> copy of B
  
  Return a copy of B with all ASCII characters converted to lowercase.

lstrip(self, bytes) -> bytearray
  Strip leading bytes contained in the argument.
  
  If the argument is omitted or None, strip leading ASCII whitespace.

maketrans(frm, to) -> Unknown
  Return a translation table useable for the bytes or bytearray translate method.
  
  The returned table will be one where each byte in frm is mapped to the byte at
  the same position in to.
  
  The bytes objects frm and to must be of the same length.

partition(self, sep) -> (bytearray, bytearray, bytearray)
  Partition the bytearray into three parts using the given separator.
  
  This will search for the separator sep in the bytearray. If the separator is
  found, returns a 3-tuple containing the part before the separator, the
  separator itself, and the part after it.
  
  If the separator is not found, returns a 3-tuple containing the original
  bytearray object and two empty bytearray objects.

pop(self, index) -> int
  Remove and return a single item from B.
  
    index
      The index from where to remove the item.
      -1 (the default value) means remove the last item.
  
  If no index argument is given, will pop the last item.

remove(self, value) -> None
  Remove the first occurrence of a value in the bytearray.
  
    value
      The value to remove.

replace(self, old, new, count) -> bytearray
  Return a copy with all occurrences of substring old replaced by new.
  
    count
      Maximum number of occurrences to replace.
      -1 (the default value) means replace all occurrences.
  
  If the optional argument count is given, only the first count occurrences are
  replaced.

reverse(self) -> None
  Reverse the order of the values in B in place.

rfind(sub, start, end) -> int
  B.rfind(sub[, start[, end]]) -> int
  
  Return the highest index in B where subsection sub is found,
  such that sub is contained within B[start,end].  Optional
  arguments start and end are interpreted as in slice notation.
  
  Return -1 on failure.

rindex(sub, start, end) -> int
  B.rindex(sub[, start[, end]]) -> int
  
  Like B.rfind() but raise ValueError when the subsection is not found.

rjust(width, fillchar) -> bytearray
  B.rjust(width[, fillchar]) -> copy of B
  
  Return B right justified in a string of length width. Padding is
  done using the specified fill character (default is a space)

rpartition(self, sep) -> (bytearray, bytearray, bytearray)
  Partition the bytes into three parts using the given separator.
  
  This will search for the separator sep in the bytearray, starting and the end.
  If the separator is found, returns a 3-tuple containing the part before the
  separator, the separator itself, and the part after it.
  
  If the separator is not found, returns a 3-tuple containing two empty bytearray
  objects and the original bytearray object.

rsplit(self, sep, maxsplit) -> [bytearray]
  Return a list of the sections in the bytearray, using sep as the delimiter.
  
    sep
      The delimiter according which to split the bytearray.
      None (the default value) means split on ASCII whitespace characters
      (space, tab, return, newline, formfeed, vertical tab).
    maxsplit
      Maximum number of splits to do.
      -1 (the default value) means no limit.
  
  Splitting is done starting at the end of the bytearray and working to the front.

rstrip(self, bytes) -> bytearray
  Strip trailing bytes contained in the argument.
  
  If the argument is omitted or None, strip trailing ASCII whitespace.

split(self, sep, maxsplit) -> [bytearray]
  Return a list of the sections in the bytearray, using sep as the delimiter.
  
    sep
      The delimiter according which to split the bytearray.
      None (the default value) means split on ASCII whitespace characters
      (space, tab, return, newline, formfeed, vertical tab).
    maxsplit
      Maximum number of splits to do.
      -1 (the default value) means no limit.

splitlines(self, keepends) -> [bytearray]
  Return a list of the lines in the bytearray, breaking at line boundaries.
  
  Line breaks are not included in the resulting list unless keepends is given and
  true.

startswith(prefix, start, end) -> bool
  B.startswith(prefix[, start[, end]]) -> bool
  
  Return True if B starts with the specified prefix, False otherwise.
  With optional start, test B beginning at that position.
  With optional end, stop comparing B at that position.
  prefix can also be a tuple of bytes to try.

strip(self, bytes) -> bytearray
  Strip leading and trailing bytes contained in the argument.
  
  If the argument is omitted or None, strip leading and trailing ASCII whitespace.

swapcase() -> bytearray
  B.swapcase() -> copy of B
  
  Return a copy of B with uppercase ASCII characters converted
  to lowercase ASCII and vice versa.

title() -> bytearray
  B.title() -> copy of B
  
  Return a titlecased version of B, i.e. ASCII words start with uppercase
  characters, all remaining cased characters have lowercase.

translate() -> bytearray
  translate(table, [deletechars])
  Return a copy with each character mapped by the given translation table.
  
    table
      Translation table, which must be a bytes object of length 256.
  
  All characters occurring in the optional argument deletechars are removed.
  The remaining characters are mapped through the given translation table.

upper() -> bytearray
  B.upper() -> copy of B
  
  Return a copy of B with all ASCII characters converted to uppercase.

zfill(width) -> bytearray
  B.zfill(width) -> copy of B
  
  Pad a numeric string B with zeros on the left, to fill a field
  of the specified width.  B is never truncated.

