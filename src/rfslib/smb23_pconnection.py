import smbprotocol as smb

from rfslib import abstract_pconnection
import socket
from os.path import split

import shutil, stat

def config_smb23(**arg):
  smb.ClientConfig(skip_dfs=arg["no_dfs"], 
       require_secure_negotiate=not arg["disable_secure_negotiate"])
  
  if 'dfs_domain_controller' in arg:
    smb.ClientConfig(domain_controller=arg['dfs_domain_controller'])

class Smb23PConnection(abstract_pconnection.PConnection):
  def __init__(self, **arg):
    super().__init__(**arg)

    self.__service_name = arg["service_name"]
    self.__host = arg["host"]
    
    smb.register_session(arg["host"], username=arg["username"], password=arg["password"],
      port=arg["port"], encrypt=arg["enable_encryption"])


  def close(self):
    self.__smb.close()

  def __prefix_path(self, path):
    return '\\\\' + self.__host + '\\' + self.__service_name

  def _listdir(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)
    return smb.listdir(p_remote_path)

  def _rename(self, old_name, new_name):
    p_old_name = self.__prefix_path(old_name)
    p_new_name = self.__prefix_path(new_name)
    
    smb.rename(p_old_name, p_new_name)

  def _push(self, local_path, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    with open(local_path, "rb") as local_file, smb.open_file(p_remote_path, "wb") as remote_file:
      shutil.copyfileobj(local_file, remote_file)

  def _pull(self, remote_path, local_path):
    p_remote_path = self.__prefix_path(remote_path)

    with smb.open_file(p_remote_path, "rb") as remote_file, open(local_path, "wb") as local_file:
      shutil.copyfileobj(remote_file, local_file)
  
  def _isdir(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    return stat.S_ISDIR(smb.stat(p_remote_path).st_mode)
  
  def _mkdir(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    smb.mkdir(p_remote_path)

  def _rmdir(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    smb.mkdir(p_remote_path)

  def _unlink(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    smb.unlink(p_remote_path)

  def _exists(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    dirname, basename = split(remote_path)
    return basename in self._listdir(dirname)
  
  def _lexists(self, remote_path):
    p_remote_path = self.__prefix_path(remote_path)

    return self._exists(remote_path)


