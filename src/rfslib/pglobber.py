# Original source file - https://github.com/python/cpython/blob/3.9/Lib/glob.py
# THIS IS UTTERLY PIGGY SOLUTION OF THE PROBLEM! DEBUGGING IS WELCOME.
# Don't use anything else then glob function - YOU HAVE BEEN WARNED.
"""Filename globbing utility."""

from os import path
import re
import fnmatch
import sys

import logging

_magic_check = re.compile('([*?[])')
_magic_check_bytes = re.compile(b'([*?[])')

class PGlobber():
  def __init__(self, connection):
    self._connection = connection

  def glob(self, pathname, *, recursive=True):
    """Return a list of paths matching a pathname pattern.
    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.
    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    logging.info("Resolving remote wildcard {}".format(pathname))
    result = list(self._iglob(pathname, recursive=recursive))

    if result == []:
      logging.warning("Wildcard {} failed resolution. Returning {}".format(pathname, pathname))
      return [pathname]
    else:

      i_result = ""
      for r in result:
        i_result += "\n" + r

      logging.info("Wildcard {} succeded resolution. Returning {}".format(pathname, i_result))
      return result

  def _iglob(self, pathname, *, recursive=False):
    """Return an iterator which yields the paths matching a pathname pattern.
    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.
    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    it = self.__iglob(pathname, recursive, False)
    if recursive and self._isrecursive(pathname):
      s = next(it)  # skip empty string
      assert not s
    return it

  def __iglob(self, pathname, recursive, dironly):
    dirname, basename = path.split(pathname)
    if not self._has_magic(pathname):
      assert not dironly
      if basename:
        if self._connection.lexists(pathname):
          yield pathname
      else:
        # Patterns ending with a slash should match only directories
        if self._connection.isdir(dirname):
          yield pathname
      return
    if not dirname:
      if recursive and self._isrecursive(basename):
        yield from self._glob2(dirname, basename, dironly)
      else:
        yield from self.__glob1(dirname, basename, dironly)
      return
    # `os.path.split()` returns the argument itself as a dirname if it is a
    # drive or UNC path.  Prevent an infinite recursion if a drive or UNC path
    # contains magic characters (i.e. r'\\?\C:').
    if dirname != pathname and self._has_magic(dirname):
      dirs = __iglob(dirname, recursive, True)
    else:
      dirs = [dirname]
    if self._has_magic(basename):
      if recursive and self._isrecursive(basename):
        self.glob_in_dir = self._glob2
      else:
        self.glob_in_dir = self.__glob1
    else:
      self.glob_in_dir = self.__glob0
    for dirname in dirs:
      for name in self.glob_in_dir(dirname, basename, dironly):
        yield path.join(dirname, name)

  # These 2 helper functions non-recursively glob inside a literal directory.
  # They return a list of basenames.  __glob1 accepts a pattern while __glob0
  # takes a literal basename (so it only has to check for its existence).

  def __glob1(self, dirname, pattern, dironly):
    names = list(self._iterdir(dirname, dironly))
    if not self._ishidden(pattern):
      names = (x for x in names if not self._ishidden(x))
    return fnmatch.filter(names, pattern)

  def __glob0(self, dirname, basename, dironly):
    if not basename:
      # `os.path.split()` returns an empty basename for paths ending with a
      # directory separator.  'q*x/' should match only directories.
      if self._connection.isdir(dirname):
        return [basename]
    else:
      if self._connection.lexists(join(dirname, basename)):
        return [basename]
    return []


  def _glob0(self, dirname, pattern):
    return __glob0(dirname, pattern, False)

  def _glob1(self, dirname, pattern):
    return __glob1(dirname, pattern, False)

  # This helper function recursively yields relative pathnames inside a literal
  # directory.

  def _glob2(self, dirname, pattern, dironly):
    assert self._isrecursive(pattern)
    yield pattern[:0]
    yield from self._rlistdir(dirname, dironly)

  # If dironly is false, yields all file names inside a directory.
  # If dironly is true, yields only directory names.
  def _iterdir(self, dirname, dironly):
    if not dirname:
      dirname = '/'
    
    for entry in self._connection.xls(dirname):
      if not dironly or self._connection.isdir(entry):
        yield path.basename(entry)
    return

  # Recursively yields relative pathnames inside a literal directory.
  def _rlistdir(self, dirname, dironly):
    names = list(self._iterdir(dirname, dironly))
    for x in names:
      if not self._ishidden(x):
        yield x
        lpath = path.join(dirname, x) if dirname else x
        for y in self._rlistdir(lpath, dironly):
          yield path.join(x, y)


  def _has_magic(self, s):
    if isinstance(s, bytes):
      match = _magic_check_bytes.search(s)
    else:
      match = _magic_check.search(s)
    return match is not None

  def _ishidden(self, path):
    return path[0] in ('.', b'.'[0])

  def _isrecursive(self, pattern):
    if isinstance(pattern, bytes):
      return pattern == b'**'
    else:
      return pattern == '**'

  def _escape(self, pathname):
    """Escape all special characters.
    """
    # Escaping is done by wrapping any of "*?[" between square brackets.
    # Metacharacters do not work in the drive part and shouldn't be _escaped.
    drive, pathname = path.splitdrive(pathname)
    if isinstance(pathname, bytes):
      pathname = _magic_check_bytes.sub(br'[\1]', pathname)
    else:
      pathname = _magic_check.sub(r'[\1]', pathname)
    return drive + pathname
