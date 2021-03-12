import pytest
import os
from classes.Certificate import Certificate

def test_init_value_error_1_arg():
    with pytest.raises(ValueError):
        Certificate('', 'cloudflare')

def test_init_value_error_2_arg():
    with pytest.raises(ValueError):
        Certificate('my-domain.com', '')

def test_init_type_error_1_arg():
    with pytest.raises(TypeError):
        Certificate(2, 'cloudflare')

def test_init_type_error_2_arg():
    with pytest.raises(TypeError):
        Certificate('my-domain.com', True)


certificate = Certificate('wiserpv.com', 'cloudflare')
# def test_cert_exists():
#     repository_dir = os.path.dirname(os.path.realpath(__file__))
#     assert certificate.exists(repository_dir) == True

def test_is_close_to_expire():
    assert certificate.is_close_to_expire() == False

def test_is_close_to_expire_300_days_left():
    assert certificate.is_close_to_expire(days_left=300) == True


# certificate = Certificate('mercurypay.io', 'cloudflare')
# def test_is_close_to_expire_before_create():
#     with pytest.raises(FileNotFoundError):
#         certificate.is_close_to_expire()

# def test_cert_exists_before_create():
#     assert certificate.exists() == False

# def test_create():
#     certificate.create()
#     assert certificate.is_close_to_expire() == False

# def test_cert_exists_after_create():
#     assert certificate.exists() == True
#