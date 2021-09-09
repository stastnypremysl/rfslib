import pytest


@pytest.fixture
def connection(username, password, host, port, connection_type, service_name, client_name, use_ntlm_v1, use_direct_tcp, enable_encryption,
  disable_secure_negotiate, no_dfs, dfs_domain_controller, dont_require_signing, tls, tls_trust_chain, passive_mode,
  connection_encoding, dont_use_list_a, direct_write, skip_validation):
  pass

def test_connect(username, connection):
  pass


def test_cp(connection_type):
  assert connection_type
