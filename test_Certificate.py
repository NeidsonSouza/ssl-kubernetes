import pytest
import os
from classes.Certificate import Certificate

repository_dir = os.path.dirname(os.path.realpath(__file__))

def test_init_value_error_1_arg():
    with pytest.raises(ValueError):
        Certificate('', 'cloudflare', repository_dir)

def test_init_value_error_2_arg():
    with pytest.raises(ValueError):
        Certificate('my-domain.com', '', repository_dir)

def test_init_type_error_1_arg():
    with pytest.raises(TypeError):
        Certificate(2, 'cloudflare', repository_dir)

def test_init_type_error_2_arg():
    with pytest.raises(TypeError):
        Certificate('my-domain.com', True, repository_dir)


certificate = Certificate('wiserpv.com', 'cloudflare', repository_dir)
def test_cert_exists():
    assert certificate.exists() == True

def test_is_close_to_expire():
    assert certificate.is_close_to_expire() == False

def test_is_close_to_expire_300_days_left():
    assert certificate.is_close_to_expire(limit_in_days=300) == True


certificate_mercury = Certificate('mercurypay.io', 'cloudflare', repository_dir)
def test_is_close_to_expire_before_create():
    with pytest.raises(FileNotFoundError):
        certificate_mercury.is_close_to_expire()

def test_cert_exists_before_create():
    assert certificate_mercury.exists() == False

def test_create():
    certificate_mercury.create('https://acme-staging-v02.api.letsencrypt.org/directory')
    assert certificate_mercury.is_close_to_expire() == False

def test_cert_exists_after_create():
    assert certificate_mercury.exists() == True
