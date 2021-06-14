import paramiko
from rfslib import abstract_pconnection

from stat import S_ISDIR

class SftpPConnection(abstract_pconnection.PConnection):
  def __init__(self, **arg):
    super().__init__(**arg)

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    
    host_key_policy = None
    if arg["strict_host_key_checking"] == False:
      host_key_policy = paramiko.client.WarningPolicy

    else:
      host_key_policy = paramiko.client.RejectPolicy

    client.set_missing_host_key_policy = host_key_policy
      
    if arg["password"] == None:
      client.connect(hostname=arg["host"], port=arg["port"], username=arg["username"], key_filename=arg["keyfile"])
    else:
      client.connect(hostname=arg["host"], port=arg["port"], username=arg["username"], password=arg["password"])

    self.__sftp = client.open_sftp()

  def close(self):
    self.__sftp.close()
  
  def _listdir(self, remote_path):
    return self.__sftp.listdir(path=remote_path)

  def _rename(self, old_name, new_name):
    self.__sftp.rename(old_name, new_name) 

  def _push(self, local_path, remote_path):
    self.__sftp.put(local_path, remote_path)

  def _pull(self, remote_path, local_path):
    self.__sftp.get(remote_path, local_path)
  
  def _isdir(self, remote_path):
    result = False
    try:
      result = S_ISDIR(self._sftp.stat(remote_path).st_mode)
    except IOError:     # no such file
      result = False
    return result
  
  def _mkdir(self, remote_path):
    self.__sftp.mkdir(remote_path, mode=744)

  def _rmdir(self, remote_path):
    self.__sftp.rmdir(remote_path)

  def _unlink(self, remote_path):
    self.__sftp.unlink(remote_path)

  def _exists(self, remote_path):
    try:
      self.__sftp.stat(remotepath)
    except IOError:
      return False

    return True
  
  def _lexists(self, remote_path):
    try:
      self._sftp.lstat(remotepath)
    except IOError:
      return False
    return True


