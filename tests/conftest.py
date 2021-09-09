def pytest_addoption(parser):

  parser.addoption('--username', help='Username, which is used to connect the file storage.')
  parser.addoption('--password', help='Password, which is used to connect the file storage.')

  parser.addoption('--host', help='The address of server.')
  parser.addoption('--port', help='The port for a connection to the file storage. Defaults to RFC standard port.', type=int)
  parser.addoption('--connection-type', help='A connection type to the file storage. (SMB12/SMB23/SFTP/FTP/FS) SMB12 is samba version 1 or 2 and SMB23 is samba version 2 or 3.', required=True, default='FS')

  parser.addoption('--service-name', help='Contains a name of shared folder. Applicable only for SMB12/SMB23.')
  parser.addoption('--client-name', help='Overrides a default RFSTOOLS client name. Applicable only for SMB12.', default='RFSTOOLS')

  parser.addoption('--use-ntlm-v1', help='Enables deprecated ntlm-v1 authentication. Applicable only for SMB12.', action='store_true')
  parser.addoption('--use-direct-tcp', help='Enables newer direct TCP connection over NetBIOS connection. Applicable only for SMB12. (don\'t forget to change port to 445)', 
          action='store_true')

  parser.addoption('--enable-encryption', help='Enables encryption for a SMB3 connection. Applicable only for SMB23.', action='store_true',)
  parser.addoption('--disable-secure-negotiate', help='Disables secure negotiate requirement for a SMB connection. Applicable only for SMB23.', action='store_true')
  parser.addoption('--no-dfs', help='Disables DFS support - useful as a bug fix. Applicable only for SMB23.', action='store_true',)
  parser.addoption('--dfs-domain-controller', help='The DFS domain controller address. Useful in case, when rfslib fails to find it themself. Applicable only for SMB23')
  parser.addoption('--dont-require-signing', help='Disables signing requirement. Applicable only for SMB23.', action='store_true')

  parser.addoption('--tls', help='Activate TLS. Applicable only for FTP.', action='store_true')
  parser.addoption('--tls-trust-chain', help='The trust chain file path for TLS. Applicable only for FTP.', action='store_true')
  parser.addoption('--passive-mode', help='Use passive mode for FTP. Applicable only for FTP.', action='store_true')
  parser.addoption('--connection-encoding', help='Sets an encoding for a FTP connection. Applicable only for FTP. Defaults to UTF8.', default='UTF8')
  parser.addoption('--dont-use-list-a', action='store_true',
    help='Disables usage of LIST -a command and uses LIST command instead. You might consider using option --direct-write when using --dont-use-list-a. Applicable only for FTP.')



options = ['username', 'password', 'host', 'port', 'connection_type', 'service_name', 'client_name', 'use_ntlm_v1', 'use_direct_tcp', 'enable_encryption',
  'disable_secure_negotiate', 'no_dfs', 'dfs_domain_controller', 'dont_require_signing', 'tls', 'tls_trust_chain', 'passive_mode',
  'connection_encoding', 'dont_use_list_a']

mixed_bool_options = ['direct_write', 'skip_validation']


def pytest_generate_tests(metafunc):
  for option in options:
    if option in metafunc.fixturenames:
      metafunc.parametrize(option, [metafunc.config.getoption(option)])

  for option in mixed_bool_options:
    if option in metafunc.fixturenames:
      metafunc.parametrize(option, [False, True])
