__add__(self, value) -> str
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

__format__(format_spec) -> str
  S.__format__(format_spec) -> str
  
  Return a formatted version of S as described by format_spec.

__ge__(self, value) -> bool
  Return self>=value.

__getattribute__(self, name) -> Unknown
  Return getattr(self, name).

__getitem__(self, key) -> str
  Return self[key].

__getnewargs__() -> Unknown

__gt__(self, value) -> bool
  Return self>value.

__hash__(self) -> int
  Return hash(self).

__init__(self) -> None
  Initialize self.  See help(type(self)) for accurate signature.

__iter__(self) -> [str]
  Implement iter(self).

__le__(self, value) -> bool
  Return self<=value.

__len__(self) -> int
  Return len(self).

__lt__(self, value) -> bool
  Return self<value.

__mod__(self, value) -> str
  Return self%value.

__mul__(self, value) -> str
  Return self*value.n

__ne__(self, value) -> bool
  Return self!=value.

__new__(type) -> str
  Create and return a new object.  See help(type) for accurate signature.

__reduce__() -> Unknown
  helper for pickle

__reduce_ex__() -> Unknown
  helper for pickle

__repr__(self) -> str
  Return repr(self).

__rmod__(self, value) -> str
  Return value%self.

__rmul__(self, value) -> str
  Return self*value.

__setattr__(self, name, value) -> None
  Implement setattr(self, name, value).

__sizeof__() -> int
  S.__sizeof__() -> size of S in memory, in bytes

__str__(self) -> str
  Return str(self).

__subclasshook__() -> bool
  Abstract classes can override this to customize issubclass().
  
  This is invoked early on by abc.ABCMeta.__subclasscheck__().
  It should return True, False or NotImplemented.  If it returns
  NotImplemented, the normal algorithm is used.  Otherwise, it
  overrides the normal algorithm (and the outcome is cached).

capitalize() -> str
  S.capitalize() -> str
  
  Return a capitalized version of S, i.e. make the first character
  have upper case and the rest lower case.

casefold() -> str
  S.casefold() -> str
  
  Return a version of S suitable for caseless comparisons.

center(width, fillchar) -> str
  S.center(width[, fillchar]) -> str
  
  Return S centered in a string of length width. Padding is
  done using the specified fill character (default is a space)

count(sub, start, end) -> int
  S.count(sub[, start[, end]]) -> int
  
  Return the number of non-overlapping occurrences of substring sub in
  string S[start:end].  Optional arguments start and end are
  interpreted as in slice notation.

encode(encoding='utf-8', errors='strict') -> bytes
  S.encode(encoding='utf-8', errors='strict') -> bytes
  
  Encode S using the codec registered for encoding. Default encoding
  is 'utf-8'. errors may be given to set a different error
  handling scheme. Default is 'strict' meaning that encoding errors raise
  a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and
  'xmlcharrefreplace' as well as any other name registered with
  codecs.register_error that can handle UnicodeEncodeErrors.

endswith(suffix, start, end) -> bool
  S.endswith(suffix[, start[, end]]) -> bool
  
  Return True if S ends with the specified suffix, False otherwise.
  With optional start, test S beginning at that position.
  With optional end, stop comparing S at that position.
  suffix can also be a tuple of strings to try.

expandtabs(tabsize) -> str
  S.expandtabs(tabsize=8) -> str
  
  Return a copy of S where all tab characters are expanded using spaces.
  If tabsize is not given, a tab size of 8 characters is assumed.

find(sub, start, end) -> int
  S.find(sub[, start[, end]]) -> int
  
  Return the lowest index in S where substring sub is found,
  such that sub is contained within S[start:end].  Optional
  arguments start and end are interpreted as in slice notation.
  
  Return -1 on failure.

format(*args, **kwargs) -> str
  S.format(*args, **kwargs) -> str
  
  Return a formatted version of S, using substitutions from args and kwargs.
  The substitutions are identified by braces ('{' and '}').

format_map(mapping) -> str
  S.format_map(mapping) -> str
  
  Return a formatted version of S, using substitutions from mapping.
  The substitutions are identified by braces ('{' and '}').

index(sub, start, end) -> int
  S.index(sub[, start[, end]]) -> int
  
  Like S.find() but raise ValueError when the substring is not found.

isalnum() -> bool
  S.isalnum() -> bool
  
  Return True if all characters in S are alphanumeric
  and there is at least one character in S, False otherwise.

isalpha() -> bool
  S.isalpha() -> bool
  
  Return True if all characters in S are alphabetic
  and there is at least one character in S, False otherwise.

isdecimal() -> bool
  S.isdecimal() -> bool
  
  Return True if there are only decimal characters in S,
  False otherwise.

isdigit() -> bool
  S.isdigit() -> bool
  
  Return True if all characters in S are digits
  and there is at least one character in S, False otherwise.

isidentifier() -> bool
  S.isidentifier() -> bool
  
  Return True if S is a valid identifier according
  to the language definition.
  
  Use keyword.iskeyword() to test for reserved identifiers
  such as "def" and "class".

islower() -> bool
  S.islower() -> bool
  
  Return True if all cased characters in S are lowercase and there is
  at least one cased character in S, False otherwise.

isnumeric() -> bool
  S.isnumeric() -> bool
  
  Return True if there are only numeric characters in S,
  False otherwise.

isprintable() -> bool
  S.isprintable() -> bool
  
  Return True if all characters in S are considered
  printable in repr() or S is empty, False otherwise.

isspace() -> bool
  S.isspace() -> bool
  
  Return True if all characters in S are whitespace
  and there is at least one character in S, False otherwise.

istitle() -> bool
  S.istitle() -> bool
  
  Return True if S is a titlecased string and there is at least one
  character in S, i.e. upper- and titlecase characters may only
  follow uncased characters and lowercase characters only cased ones.
  Return False otherwise.

isupper() -> bool
  S.isupper() -> bool
  
  Return True if all cased characters in S are uppercase and there is
  at least one cased character in S, False otherwise.

join(iterable) -> str
  S.join(iterable) -> str
  
  Return a string which is the concatenation of the strings in the
  iterable.  The separator between elements is S.

ljust(width, fillchar) -> str
  S.ljust(width[, fillchar]) -> str
  
  Return S left-justified in a Unicode string of length width. Padding is
  done using the specified fill character (default is a space).

lower() -> str
  S.lower() -> str
  
  Return a copy of the string S converted to lowercase.

lstrip(chars) -> str
  S.lstrip([chars]) -> str
  
  Return a copy of the string S with leading whitespace removed.
  If chars is given and not None, remove characters in chars instead.

maketrans(x, y, z) -> Unknown
  Return a translation table usable for str.translate().
  
  If there is only one argument, it must be a dictionary mapping Unicode
  ordinals (integers) or characters to Unicode ordinals, strings or None.
  Character keys will be then converted to ordinals.
  If there are two arguments, they must be strings of equal length, and
  in the resulting dictionary, each character in x will be mapped to the
  character at the same position in y. If there is a third argument, it
  must be a string, whose characters will be mapped to None in the result.

partition(sep) -> (str, str, str)
  S.partition(sep) -> (head, sep, tail)
  
  Search for the separator sep in S, and return the part before it,
  the separator itself, and the part after it.  If the separator is not
  found, return S and two empty strings.

replace(old, new, count) -> str
  S.replace(old, new[, count]) -> str
  
  Return a copy of S with all occurrences of substring
  old replaced by new.  If the optional argument count is
  given, only the first count occurrences are replaced.

rfind(sub, start, end) -> int
  S.rfind(sub[, start[, end]]) -> int
  
  Return the highest index in S where substring sub is found,
  such that sub is contained within S[start:end].  Optional
  arguments start and end are interpreted as in slice notation.
  
  Return -1 on failure.

rindex(sub, start, end) -> int
  S.rindex(sub[, start[, end]]) -> int
  
  Like S.rfind() but raise ValueError when the substring is not found.

rjust(width, fillchar) -> str
  S.rjust(width[, fillchar]) -> str
  
  Return S right-justified in a string of length width. Padding is
  done using the specified fill character (default is a space).

rpartition(sep) -> (str, str, str)
  S.rpartition(sep) -> (head, sep, tail)
  
  Search for the separator sep in S, starting at the end of S, and return
  the part before it, the separator itself, and the part after it.  If the
  separator is not found, return two empty strings and S.

rsplit(sep, maxsplit=-1) -> [str]
  S.rsplit(sep=None, maxsplit=-1) -> list of strings
  
  Return a list of the words in S, using sep as the
  delimiter string, starting at the end of the string and
  working to the front.  If maxsplit is given, at most maxsplit
  splits are done. If sep is not specified, any whitespace string
  is a separator.

rstrip(chars) -> str
  S.rstrip([chars]) -> str
  
  Return a copy of the string S with trailing whitespace removed.
  If chars is given and not None, remove characters in chars instead.

split(sep, maxsplit=-1) -> [str]
  S.split(sep=None, maxsplit=-1) -> list of strings
  
  Return a list of the words in S, using sep as the
  delimiter string.  If maxsplit is given, at most maxsplit
  splits are done. If sep is not specified or is None, any
  whitespace string is a separator and empty strings are
  removed from the result.

splitlines(keepends) -> [str]
  S.splitlines([keepends]) -> list of strings
  
  Return a list of the lines in S, breaking at line boundaries.
  Line breaks are not included in the resulting list unless keepends
  is given and true.

startswith(prefix, start, end) -> bool
  S.startswith(prefix[, start[, end]]) -> bool
  
  Return True if S starts with the specified prefix, False otherwise.
  With optional start, test S beginning at that position.
  With optional end, stop comparing S at that position.
  prefix can also be a tuple of strings to try.

strip(chars) -> str
  S.strip([chars]) -> str
  
  Return a copy of the string S with leading and trailing
  whitespace removed.
  If chars is given and not None, remove characters in chars instead.

swapcase() -> str
  S.swapcase() -> str
  
  Return a copy of S with uppercase characters converted to lowercase
  and vice versa.

title() -> str
  S.title() -> str
  
  Return a titlecased version of S, i.e. words start with title case
  characters, all remaining cased characters have lower case.

translate(table) -> str
  S.translate(table) -> str
  
  Return a copy of the string S in which each character has been mapped
  through the given translation table. The table must implement
  lookup/indexing via __getitem__, for instance a dictionary or list,
  mapping Unicode ordinals to Unicode ordinals, strings, or None. If
  this operation raises LookupError, the character is left untouched.
  Characters mapped to None are deleted.

upper() -> str
  S.upper() -> str
  
  Return a copy of S converted to uppercase.

zfill(width) -> str
  S.zfill(width) -> str
  
  Pad a numeric string S with zeros on the left, to fill a field
  of the specified width. The string S is never truncated.

