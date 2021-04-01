import pytest
import os
from functions.functions import get_cert_before_creation
from classes.Certificate import Certificate


def test_init_missing_arg():
    with pytest.raises(ValueError):
        Certificate('', 'cloudflare')


def test_init_type_error_first_arg():
    with pytest.raises(TypeError):
        Certificate(0, 'cloudflare')


def test_init_type_error_second_arg():
    with pytest.raises(TypeError):
        Certificate('my-domain.com', True)


@pytest.fixture
def cert_before_creation():
    cert = Certificate('wiserpv.com', 'cloudflare')
    return get_cert_before_creation(cert)


def test_cert_exists_before_create(cert_before_creation):
    assert cert_before_creation.exists() == False


def test_is_close_to_expire_before_create(cert_before_creation):
    with pytest.raises(FileNotFoundError):
        cert_before_creation.is_close_to_expire()


def test_cert_exists_after_create(cert_before_creation):
    cert_before_creation.create()
    assert cert_before_creation.exists() == True


def test_is_close_to_expire_after_create(cert_before_creation):
    cert_before_creation.create()
    assert cert_before_creation.is_close_to_expire() == False


def test_is_close_to_expire_300_days_left(cert_before_creation):
    cert_before_creation.create()
    assert cert_before_creation.is_close_to_expire(limit_in_days=300) == True
