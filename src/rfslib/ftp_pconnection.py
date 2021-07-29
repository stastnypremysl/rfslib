from rfslib import abstract_pconnection
import ftplib
import ftputil

from os.path import split

class FtpPConnection(abstract_pconnection.PConnection):
  def __init__(self, **arg):
    super().__init__(**arg)

    if arg['tls']:
      factory_b_class = ftplib.FTP_TLS
    else:
      factory_b_class = ftplib.FTP

    session_factory = ftputil.session.session_factory(
      base_class = factory_b_class,
      port = arg['port'],
      encrypt_data_channel = arg['tls'],
      encoding = 'UTF-8',
      use_passive_mode = arg['passive_mode'],
      debug_level=1)

    self.__ftp = ftputil.FTPHost(arg['host'], arg['username'], arg['password'], session_factory=session_factory)


  def close(self):
    self.__ftp.close()
  
  def _listdir(self, remote_path):
    return self.__ftp.listdir(remote_path)

  def _rename(self, old_name, new_name):
    self.__ftp.rename(old_name, new_name) 

  def _push(self, local_path, remote_path):
    self.__ftp.upload(local_path, remote_path)

  def _pull(self, remote_path, local_path):
    self.__ftp.download(remote_path, local_path)
  
  def _isdir(self, remote_path):
    return self.__ftp.path.isdir(remote_path)
  
  def _mkdir(self, remote_path):
    self.__ftp.mkdir(remote_path)

  def _rmdir(self, remote_path):
    self.__ftp.rmdir(remote_path)

  def _unlink(self, remote_path):
    self.__ftp.unlink(remote_path)

  def _exists(self, remote_path):
    self.__ftp.path.exists(remote_path)
  
  def _lexists(self, remote_path):
     return self._exists(remote_path)


