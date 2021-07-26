from rfslib import abstract_pconnection
import ftplib

from os.path import split

class FtpPConnection(abstract_pconnection.PConnection):
  def __init__(self, **arg):
    super().__init__(**arg)

    if arg['tls']:
      self.__ftp = ftplib.FTP_TLS()
    else:
      self.__ftp = ftplib.FTP()

    self.__ftp.connect(host=arg["host"], port=arg["port"])
    self.__ftp.login(user=arg["username"], passwd=arg["password"])

  def close(self):
    self.__ftp.quit()
  
  def _listdir(self, remote_path):
    return self.__ftp.dir(remote_path)

  def _rename(self, old_name, new_name):
    self.__ftp.rename(old_name, new_name) 

  def _push(self, local_path, remote_path):
    local_file = open(local_path, "rb")
    self.__ftp.storbinary("STOR " + remote_path, local_file)

  def _pull(self, remote_path, local_path):
    local_file = open(local_path, "wbx")
    self.__ftp.retrbinary("RETR " + remote_path, local_file)
  
  def _isdir(self, remote_path):
    dirname, basename = split(remote_path)
    m = dict(self.__ftp.mlsd(remote_path, facts["type"]))
    
    return m[basename]['type'] == 'dir'
  
  def _mkdir(self, remote_path):
    self.__ftp.mkd(remote_path)

  def _rmdir(self, remote_path):
    self.__ftp.rmd(remote_path)

  def _unlink(self, remote_path):
    self.__ftp.delete(remote_path)

  def _exists(self, remote_path):
    dirname, basename = split(remote_path)
    return basename in self._listdir(dirname)
  
  def _lexists(self, remote_path):
     return self._exists(remote_path)


