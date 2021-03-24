import pytest
import os
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
def mercurypay_cert():
    return Certificate('mercurypay.io', 'cloudflare')

@pytest.fixture
def get_cert_before_creation(mercurypay_cert):
    mercurypay_cert.rm_domain_conf_file
    return mercurypay_cert

@pytest.fixture
def get_cert_before_creation(mercurypay_cert):
    # archive_dir = 'letsencrypt/archive/{}*'.format(mercurypay_cert.domain)
    # conf_file = 'letsencrypt/renewal/{}.conf'.format(mercurypay_cert.domain)
    # files_to_be_removed = [mercurypay_cert.live_dir, archive_dir, conf_file]
    # rm_files(files_to_be_removed)
    # return mercurypay_cert
    mercurypay_cert._Certificate__rm_domain_conf_file()
    return mercurypay_cert


def rm_files(files):
    for filename in files:
        if os.path.exists(filename):
            os.system('rm -rf {}'.format(filename))


def test_cert_exists_before_create(get_cert_before_creation):
    assert get_cert_before_creation.exists() == False


def test_is_close_to_expire_before_create(get_cert_before_creation):
    with pytest.raises(FileNotFoundError):
        get_cert_before_creation.is_close_to_expire()

def test_cert_exists_after_create(get_cert_before_creation):
    get_cert_before_creation.create()
    assert get_cert_before_creation.exists() == True

def test_is_close_to_expire_after_create(get_cert_before_creation):
    get_cert_before_creation.create()
    assert get_cert_before_creation.is_close_to_expire() == False

def test_is_close_to_expire_300_days_left(get_cert_before_creation):
    get_cert_before_creation.create()
    assert get_cert_before_creation.is_close_to_expire(limit_in_days=300) == True
