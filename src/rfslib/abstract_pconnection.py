from abc import ABC, abstractmethod
from typing import List

#import pysmb

import tempfile
import os
import os.path
import shutil
import codecs

from rfslib.path_utils import path_normalize

import random

import logging, sys

class p_connection_settings():
  '''This object represents settings appliable for all PConnection instances (instances of class, which inherits from PConnection).'''
  def __init__():
    '''The constructor inicializes the class to default values.'''
    pass
  
  text_transmission:bool = False
  '''If true, all files, which will be transmitted, will be recoded from local_encoding to remote_encoding and from local_crlf to remote_crlf. If False, there will be no encoding done during transmission.'''

  local_encoding:str = 'UTF8'
  '''The encoding of local text files. (eg. 'UTF8')'''
  remote_encoding:str = 'UTF8'
  '''The encoding of remote text files. (eg. 'cp1250')'''

  local_crlf:bool = False
  '''Does local files use CRLF? If True, it is supposed, they do. If False, it is supposed, they use LF.'''
  remote_crlf:bool = False
  '''Does remote files use CRLF? If True, it is supposed, they do. If False, it is supposed, they use LF.'''

  direct_write:bool = False
  '''NOT IMPLEMENTED YET. If True, push will write output directly to file. If False all push operations on regular files will create firstly tmp file in target folder and then move result to file.'''

  skip_validation:bool = False
  '''NOT IMPLEMENTED YED. If True, all validations of input will be skipped. Undefined behavior may happen if input is wrong. Increses performance.'''


class PConnection(ABC):
  def set_settings(self, settings: p_connection_settings):
    '''The procedure sets all generic settings for PConnection.

    Args:
      settings: A p_connection_settings object with all generic settings for PConnection.
    '''

    self.__text_transmission = settings.text_transmission

    self.__local_encoding = settings.local_encoding
    self.__remote_encoding = settings.remote_encoding

    self.__local_crlf = settings.local_crlf
    self.__remote_crlf = settings.remote_crlf

    self.__direct_write = settings.direct_write

    self.__skip_validation = settings.skip_validation

  def get_settings(self) -> p_connection_settings:
    '''The procedure sets all generic settings for PConnection.

    Returns:
      A p_connection_settings object with all generic settings of PConnection.
    '''
    ret = p_connection_settings()

    ret.text_transmission = self.__text_transmission

    ret.local_encoding = self.__local_encoding
    ret.remote_encoding = self.__remote_encoding

    ret.local_crlf = self.__local_crlf
    ret.remote_crlf = self.__remote_crlf

    ret.direct_write = self.__direct_write

    ret.skip_validation = self.__skip_validation

    return ret
 
  def __init__(self, settings: p_connection_settings):
    """The constructor of a abstract class. If it is not called from child class, the behavior is undefined.

    If local_encoding and remote_encoding have same values, no recoding is done. Analogically if local_crlf and remote_crlf is same, no substitution between LF and CRLF is done.

    Args:
      settings: A p_connection_settings object with all generic settings for PConnection.

    :meta public:
    """

    self.set_settings(settings)
    

  @abstractmethod
  def close(self):
    """Method to close the opened connection."""
    pass

  @abstractmethod
  def _stat(self, remote_path: str) -> os.stat_result:
    """Protected method which returns statistics of a file (eg. size, last date modified,...) Follows symlinks to a destination file.
    Undefined behavior if remote file doesn't exist or it is a broken symlink.
    
    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file exist. False, if remote file doesn't exist.

    :meta public:
    """
    pass

  @abstractmethod
  def _lstat(self, remote_path: str) -> os.stat_result:
    """Protected method which returns statistics of a file (eg. size, last date modified,...)  Doesn't follow symlinks.
    Undefined behavior if remote file doesn't exist.
    
    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file is exist. False, if remote file doesn't exist.

    """
    pass

  @abstractmethod
  def _listdir(self, remote_path:str) -> List[str]: 
    """Protected method which returns a list of files in the folder including hidden files.
    Undefined if the remote file doesn't exist or isn't a folder.

    Args:
      remote_path: The remote path of a remote folder.

    Returns:
      List of files in the remote folder
      
    :meta public: 
    """
    pass

  @abstractmethod
  def _rename(self, old_name:str, new_name:str):
    """Protected method which renames/moves a file. Behavior is undefined, if `new_name` file exists or `old_name` file doesn't exist.

    Args:
      old_name: Remote path a file to move.
      new_name: Remote path to which move the file.
      
    :meta public: 
    """

    pass

  @abstractmethod
  def _push(self, local_path:str, remote_path:str):
    """Protected method which uploads/pushes a nondirectory file from a local storage to a remote storage in the binary form. Behavior is undefined if destination folder or source file doesn't exist, source is directory or remote file already exists.

    Args:
      local_path: Path of a local file to upload.
      remote_path: Path on the remote storage, where to upload/push a local file.
      
    :meta public: 
    """
    pass

  @abstractmethod
  def _pull(self, remote_path:str, local_path:str):
    """Protected method which downloads/pulls a nondirectory file from a remote storage to a local storage in the binary form. Behavior is undefined if source file or destination folder doesn't exist.

    Args:
      remote_path: Path of a remote file to download.
      local_path: Path of a local file, where to download/pull a remote file or local file already exists.
      
    :meta public: 
    """
    pass
  
  @abstractmethod
  def _isdir(self, remote_path:str) -> bool:
    """Protected method which checks, whether a remote file is a directory.

    Args:
      remote_path: A path of a directory.

    Returns:
      True, if remote file is folder. False, if it isn't a folder. Undefined if the file doesn't exist.

    :meta public: 
    """

    pass
  
  @abstractmethod
  def _mkdir(self, remote_path:str):
    """Protected method which creates a new directory. Behavior is undefined if remote folder already exist, or destination folder doesn't exist.

    Args:
      remote_path: A path of a new remote directory.

    :meta public: 
    """
    pass

  @abstractmethod
  def _rmdir(self, remote_path:str):
    """Protected method which removes an empty remote directory. Behavior is undefined if remote directory doesn't exist or it isn't empty.

    Args:
      remote_path: Path of an empty remote directory to delete.

    :meta public: 
    """   
    pass

  @abstractmethod
  def _unlink(self, remote_path:str):
    """Protected method which removes a nondirectory file. Behavior is undefined if remote file doesn't exist or is a directory.

    Args:
      remote_path: Path of a remote regular file to delete.

    :meta public: 
    """
    pass

  @abstractmethod
  def _exists(self, remote_path:str) -> bool:
    """Protected method which checks, whether a remote file exist. If the remote file is a broken symlink, it returns False.

    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file is exist. False, if remote file doesn't exist

    :meta public: 
    """
    pass

  @abstractmethod
  def _lexists(self, remote_path:str) -> bool:
    """Protected method which checks, whether a remote file exist. If the remote file is a broken symlink, it returns True.
    
    KNOWN BUG: Behavior is undefined in case of broken symlinks. 

    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file is exist. False, if remote file doesn't exist

    :meta public: 
    """
 
    pass

  def exists(self, remote_path:str) -> bool:
    """Method which checks, whether a remote file exist. Returns False for broken symlinks.
    
    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file exists. False, if remote file doesn't exist.

    """

    logging.debug("Does remote file {} exist?".format(remote_path))

    remote_path = path_normalize(remote_path)
    ret = self._exists(remote_path)

    logging.debug("Remote file {} exists: {}".format(remote_path, ret))
    return ret

  def lexists(self, remote_path):
    """Method which checks, whether a remote file exist. Returns True for broken symlinks.
    
    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file exists. False, if remote file doesn't exist.

    """
    logging.debug("Does remote file {} lexist?".format(remote_path))

    remote_path = path_normalize(remote_path)
    ret = self._lexists(remote_path)

    logging.debug("Remote file {} lexists: {}".format(remote_path, ret))
    return ret

  def __check_link_existance(self, remote_path):
    if not self.lexists(remote_path):
      raise FileNotFoundError("Remote file {} not found.".format(remote_path))

  def __check_file_existance(self, remote_path):
    self.__check_link_existance(remote_path)

    if not self.exists(remote_path):
      raise FileNotFoundError("Remote file {} is a broken symlink.".format(remote_path))


  def __check_file_nonexistance(self, remote_path):
    if self._lexists(remote_path):
      raise InterruptedError("Remote destination file {} exists.".format(remote_path))

  def __check_not_folder(self, remote_path):
    self.__check_file_existance(remote_path)

    if self._isdir(remote_path):
      raise IsADirectoryError("Remote file {} is a directory.".format(remote_path))

  def __check_potencial_not_folder(self, remote_path):
    if self._lexists(remote_path) and self._isdir(remote_path):
      raise IsADirectoryError("Remote file {} is a directory.".format(remote_path))
  
  def __check_is_folder(self, remote_path):
    self.__check_file_existance(remote_path)

    if not self._isdir(remote_path):
      raise NotADirectoryError("Remote file {} is not a directory.".format(remote_path))


  def __check_local_file_existance(self, local_path):
    if not os.path.lexists(local_path):
      raise FileNotFoundError("Local file {} not found.".format(local_path))
    
    if not os.path.exists(local_path):
      raise FileNotFoundError("Local file {} is a broken symlink.".format(local_path))
    
  def __check_local_file_nonexistance(self, local_path):
    if os.path.lexists(local_path):
      raise InterruptedError("Local destination file {} exists.".format(local_path))

  def __check_local_file_not_folder(self, local_path):
    self.__check_local_file_existance(local_path)
    if os.path.isdir(local_path):
      raise IsADirectoryError("Local file {} is a directory.".format(local_path))
      
  def __check_local_potencial_file_not_folder(self, local_path):
    if os.path.lexists(local_path) and os.path.isdir(local_path):
      raise IsADirectoryError("Local file {} is a directory.".format(local_path))

  def stat(self, remote_path: str) -> os.stat_result:
    """Returns statistics of a file (eg. size, last date modified,...) Follows symlinks to a destination file.
    
    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file exist. False, if remote file doesn't exist.

    """
    self.__check_file_existance(remote_path)
    return self._stat(remote_path)

  def lstat(self, remote_path: str) -> os.stat_result:
    """Returns statistics of a file (eg. size, last date modified,...)  Doesn't follow symlinks.
    
    Args:
      remote_path: Path of a remote file.

    Returns:
      True, if remote file is exist. False, if remote file doesn't exist.

    """
    self.__check_link_existance(remote_path)
    return self._lstat(remote_path)

  def __encode(self, from_lpath, to_lpath):
    if self.__text_transmission:

      with open(from_lpath, 'rb') as inp, open(to_lpath, 'wb') as out:
        inp = inp.read()
        decoded = codecs.decode(inp, encoding="utf8")

        if self.__remote_crlf:
          decoded = decoded.replace('\n', '\r\n')
        
        bout = codecs.encode(decoded, encoding=self.__remote_encoding)
        out.write(bout)

    else:
      shutil.copyfile(from_lpath, to_lpath)

  def __decode(self, from_lpath, to_lpath):
    if self.__text_transmission:
      with open(from_lpath, 'rb') as inp, open(to_lpath, 'wb') as out:
        binp = inp.read()
        decoded = codecs.decode(binp, encoding=self.__remote_encoding)

        if self.__remote_crlf:
          decoded = decoded.replace('\r\n', '\n')
        
        bout = codecs.encode(decoded, encoding="utf8")
        out.write(bout)
    else:
      shutil.copyfile(from_lpath, to_lpath)

  def __infolder_tmp_file(self, path):
    dirname, basename = os.path.split(path)
    return os.path.join(dirname, '.' + basename + '.tmp' + str(random.randint(10000,65555)))
    

  def push(self, local_path, remote_path):
    """Uploads/pushes a file from a local storage to a remote storage in the binary form.

    Args:
      local_path: Path of a local file to upload.
      remote_path: Path on the remote storage, where to upload/push a local file.
      
    :meta public: 
    """

    logging.debug("Pushing local file {} to the remote file {}.".format(local_path, remote_path))

    remote_path = path_normalize(remote_path)
    local_path = path_normalize(local_path)
    
    self.__check_local_file_not_folder(local_path)
    self.__check_potencial_not_folder(remote_path)

    with tempfile.NamedTemporaryFile() as _tmp_file:
      tmp_file = _tmp_file.name
    
      self.__encode(local_path, tmp_file)

      tmp_file2 = self.__infolder_tmp_file(remote_path)
      self._push(tmp_file, tmp_file2)
      self.fmv(tmp_file2, remote_path)

    logging.debug("Pushing local file {} to the remote file {} is completed.".format(local_path, remote_path))

  #recursive push
  def rpush(self, local_path, remote_path):
    logging.debug("Recursive pushing of local file {} to the remote file {}.".format(local_path, remote_path))

    remote_path = path_normalize(remote_path)
    local_path = path_normalize(local_path)

    self.__check_local_file_existance(local_path)

    if os.path.isdir(local_path):
      if self.lexists(remote_path): 
        if not self.isdir(remote_path):
          raise InterruptedError("Cannot upload a folder {} to a non-folder path {}".format(local_path, remote_path))
        else:
          self.mkdir(remote_path)
        
      for l_file in os.listdir(local_path):
        self.rpush(os.path.join(local_path, l_file), os.path.join(remote_path, l_file))
        
    else:
      if self.lexists(remote_path): 
        if self.isdir(remote_path):
          raise InterruptedError("Cannot upload a non-folder {} to a folder path {}".format(local_path, remote_path))

      self.push(local_path, remote_path)

    logging.debug("Recursive pushing of local file {} to the remote file {} is completed.".format(local_path, remote_path))


  def pull(self, remote_path, local_path):
    logging.debug("Pulling remote file {} to the local file {}.".format(remote_path, local_path))

    remote_path = path_normalize(remote_path)
    local_path = path_normalize(local_path)

    self.__check_not_folder(remote_path)
    self.__check_local_potencial_file_not_folder(local_path)

    with tempfile.NamedTemporaryFile() as _tmp_file:
      tmp_file = _tmp_file.name
       
      self._pull(remote_path, tmp_file)

      tmp_file2 = self.__infolder_tmp_file(local_path)
      self.__decode(tmp_file, tmp_file2)

      shutil.move(tmp_file2, local_path)

    logging.debug("Pulling remote file {} to the local file {} is completed.".format(remote_path, local_path))

  #recursive pull
  def rpull(self, remote_path, local_path):
    logging.debug("Recursive pulling of remote file {} to the local file {}.".format(remote_path, local_path))

    remote_path = path_normalize(remote_path)
    local_path = path_normalize(local_path)

    self.__check_file_existance(remote_path)
    
    if self.isdir(remote_path):
      if os.path.lexists(local_path):
        if not os.path.isdir(local_path):
          raise InterruptedError("Cannot download a folder {} to a non-folder path {}".format(remote_path, local_path))
      else:
        os.mkdir(local_path)
      
      for r_file in self.ls(remote_path):
        self.rpull(os.path.join(remote_path, r_file), os.path.join(local_path, r_file))
        
    else:
      if os.path.lexists(local_path):
        if os.path.isdir(local_path):
          raise InterruptedError("Cannot download a non-folder {} to a folder path {}".format(remote_path, local_path))
      
      self.pull(remote_path, local_path)
      
    logging.debug("Recursive pulling of remote file {} to the local file {} is completes.".format(remote_path, local_path))
  
  def listdir(self, remote_path):
    logging.debug("Listing file {}.".format(remote_path))

    remote_path = path_normalize(remote_path)
    self.__check_is_folder(remote_path)
    
    return self._listdir(remote_path)


  def find(self, remote_path, child_first=False):
    logging.debug("Finding (making a tree) of file {}.".format(remote_path))

    remote_path = path_normalize(remote_path)
    self.__check_file_existance(remote_path)

    if self._isdir(remote_path):
      ret = []
      for f in self.xls(remote_path):
        if not child_first:
          ret.append(remote_path)

        ret.extend( dfs_find(self, f) )

        if child_first:
          ret.append(remote_path)
        
    else:
      return [remote_path]

  def mkdir(self, remote_path):
    logging.debug("Making a directory file {}.".format(remote_path))

    remote_path = path_normalize(remote_path)
    self.__check_file_nonexistance(remote_path)

    self._mkdir(remote_path)

    logging.debug("Making a directory file {} is completed.".format(remote_path))

  # Recursive mkdir
  def pmkdir(self, remote_path):
    logging.debug("Recursive making of a directory file {}.".format(remote_path))

    remote_path = path_normalize(remote_path)

    if self.lexists(remote_path):
      if self.isdir(remote_path):
        return
      else:
        raise InterruptedError("File {} is not a folder.".format(remote_path))

    dirname, basename = os.path.split(remote_path)
    self.pmkdir(dirname)
    self.mkdir(remote_path)

    logging.debug("Recursive making of a directory file {} is completed.".format(remote_path))
    

  def rmdir(self, remote_path):
    logging.debug("Removing remote empty directory file {}.".format(remote_path))

    remote_path = path_normalize(remote_path)
    self.__check_is_folder(remote_path)

    if not self.ls(remote_path) == []:
      raise InterruptedError("Remote folder is not empty.")

    self._rmdir(remote_path)

    logging.debug("Removing remote empty directory file {} is completed".format(remote_path))

  def rename(self, old_name, new_name):
    logging.debug("Renaming remote file {} to {}.".format(old_name, new_name))

    old_name = path_normalize(old_name)
    new_name = path_normalize(new_name)

    self.__check_file_existance(old_name)
    self.__check_file_nonexistance(new_name)

    self._rename(old_name, new_name)

    logging.debug("Renaming remote file {} to {} is completed.".format(old_name, new_name))

  # mv one non-dircetory file to a non-directory file
  def fmv(self, old_name, new_name):
    logging.debug("Moving remote non-directory file {} to a remote non-directory file {}.".format(old_name, new_name))

    self.__check_not_folder(old_name)
    self.__check_potencial_not_folder(old_name)

    if self.exists(new_name):
      self.rm(new_name)
    
    self.rename(old_name, new_name)

    logging.debug("Moving remote non-directory file {} to a remote non-directory file {} is completed.".format(old_name, new_name))
  
  # mv to dir
  def dmv(self, old_names, target_dir):
    logging.debug("Moving remote file {} inside a remote target directory {}.".format(old_names, target_dir))

    old_names = [*map(path_normalize, old_names)]
    target_dir = path_normalize(target_dir)
    
    self.__check_is_folder(target_dir)
    for name in old_names:
      self.__check_file_existance(name)   

    target_dir_ls = self.ls(target_dir)

    for name in old_names:
      dirname, basename = os.path.split(name)
      newname = os.path.join(target_dir, basename)

      if self.isdir(name):
        if basename in target_dir_ls:
          if not self.isdir(newname):
            raise InterruptedError("Cannot overwrite remote non-directory {} with remote directory {}.".format(newname, name))
          self.dmv(self.xls(name), newname)

        else:
          self.rename(name, newname)          
     
      else:
        if basename in target_dir_ls:
          if self.isdir(newname):
            raise InterruptedError("Cannot overwrite remote directory {} with remote non-directory {}.".format(newname, name))
        
        self.fmv(name, newname)

    logging.debug("Moving remote files {} inside a remote directory {} is completed.".format(old_names, new_name))


  def mv(self, old_names, new_name):
    logging.debug("Moving remote file {} to a remote destination {}.".format(old_names, new_name))

    if self.lexists(new_name) and self.isdir(new_name):
      self.dmv(old_names, new_name)

    else:
      if len(old_names) == 0:
        return
      elif len(old_names) > 1:
        if self.exists(new_name):
          raise InterruptedError("Cannot move more than 1 file to non-directory {}.".format(new_name))
        else:
          raise InterruptedError("Cannot move more than 1 file to non-existent location {}.".format(new_name))
      else:
        if self.isdir(old_names[0]):
          self.rename(old_names[0], new_name)
        else:
          self.fmv(old_names[0], new_name)

    logging.debug("Moving remote file {} to a remote destination {} is completed.".format(old_names, new_name))
          

  def fcp(self, old_name, new_name):
    logging.debug("Copying remote non-directory file {} to a remote non-directory file {}.".format(old_name, new_name))

    self.__check_not_folder(old_name)
    self.__check_potencial_not_folder(old_name)
    
    with tempfile.NamedTemporaryFile() as _tmp_file:
      tmp_file = _tmp_file.name
      self.pull(old_name, tmp_file)
    
      if self.exists(new_name):
        self.rm(new_name)
      self.push(tmp_file, new_name)

    logging.debug("Copying remote non-directory file {} to a remote non-directory file {} is completed.".format(old_name, new_name))

  def dcp(self, old_names, target_dir, recursive=False):
    logging.debug("Copying remote file {} inside a remote directory {}. (recursive={})".format(old_names, target_dir, recursive))

    old_names = [*map(path_normalize, old_names)]
    target_dir = path_normalize(target_dir)

    self.__check_is_folder(target_dir)
    for name in old_names:
      if not recursive:
        self.__check_not_folder(name)
      else:
        self.__check_file_existance(name)   
    
    target_dir_ls = self.ls(target_dir)


    for name in old_names:
      dirname, basename = os.path.split(name)
      newname = os.path.join(target_dir, basename)

      logging.debug("New name of remote file {} will be {}.".format(name, newname))

      if recursive and self.isdir(name):
        if basename in target_dir_ls:
          if not self.isdir(newname):
            raise InterruptedError("Cannot overwrite remote non-directory {} with remote directory {}.".format(newname, name))

        else:
          self.mkdir(newname)   
       
        self.dcp(self.xls(name), newname)
     
      else:
        if basename in target_dir_ls:
          if self.isdir(newname):
            raise InterruptedError("Cannot overwrite remote directory {} with remote non-directory {}.".format(newname, name))
        
        self.fcp(name, newname)

    logging.debug("Copying remote file {} inside a remote directory {} is completed. (recursive={})".format(old_names, target_dir, recursive))



  def cp(self, old_names, new_name, recursive=False):
    logging.debug("Copying remote files {} to destination {} (recursive={}).".format(old_names, new_name, recursive))

    if self.exists(new_name) and self.isdir(new_name):
      self.dcp(old_names, new_name, recursive=recursive)

    else:
      if len(old_names) == 0:
        return
      elif len(old_names) > 1:
        if self.exists(new_name):
          raise InterruptedError("Cannot copy more than 1 file to non-directory {}.".format(new_name))
        else:
          raise InterruptedError("Cannot copy more than 1 file to non-existent location {}.".format(new_name))
      else:
        self.fcp(old_names[0], new_name)

    logging.debug("Copying remote files {} to destination {} is completed (recursive={}).".format(old_names, new_name, recursive))
 
  
  def unlink(self, remote_path):
    logging.debug("Unlinking remote non-directory file {}".format(remote_path))     

    remote_path = path_normalize(remote_path)
    self.__check_not_folder(remote_path)

    self._unlink(remote_path)

    logging.debug("Unlinking remote non-directory file {} is completed".format(remote_path))     

  def isdir(self, remote_path):
    logging.debug("Is remote file {} a directory?".format(remote_path))     

    remote_path = path_normalize(remote_path)
    self.__check_file_existance(remote_path)

    ret = self._isdir(remote_path)
    logging.debug("Remote file {} is a directory: {}".format(remote_path, ret)) 

    return ret    

  def rm(self, remote_path, recursive=False):
    logging.debug("Deleting remote non-directory file {} (recursive={})".format(remote_path, recursive))     

    remote_path = path_normalize(remote_path)
    self.__check_file_existance(remote_path)

    if not recursive:
      self.unlink(remote_path)
    
    else:
      for f in self.find(remote_path, child_first=True):
        if self.isdir(f):
          self.rmdir(f)
        else: 
          self.unlink(f)

    logging.debug("Deleting remote non-directory file {} is completed (recursive={})".format(remote_path, recursive))     
       

  def ls(self, remote_path):
    logging.debug("Listing remote directory file {}".format(remote_path))     

    remote_path = path_normalize(remote_path)
    self.__check_file_existance(remote_path)
    
    ret = []
    
    if self.isdir(remote_path):
      ret = self.listdir(remote_path)
    else:
      ret = [os.path.basename(remote_path)]

    logging.debug("Remote directory file {} contains {}.".format(remote_path, ret))
    return ret

  # xls returns list of children with dirname
  def xls(self, remote_path):
    remote_path = path_normalize(remote_path)

    def prepend_d(lfile):
      return os.path.join(remote_path, lfile)

    if self.isdir(remote_path):
      return map(prepend_d, self.ls(remote_path))
    else: 
      return [remote_path]

  def touch(self, remote_path):
    with tempfile.NamedTemporaryFile() as _tmp_file:
      tmp_file = _tmp_file.name
      self.push(tmp_file, remote_path)    
  
  def __enter__(self):
      return self

  def __exit__(self, exc_type, exc_val, exc_tb):
      self.close()





