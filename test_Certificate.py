import pytest
import os
from classes.Certificate import Certificate
from dotenv import load_dotenv

load_dotenv('.env.dev')
os.environ['APP_ROOT_DIR'] = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.getenv('APP_ROOT_DIR'))

@pytest.fixture
def repository_dir():
    return os.path.dirname(os.path.realpath(__file__))


def test_init_missing_arg(repository_dir):
    with pytest.raises(ValueError):
        Certificate('', 'cloudflare', repository_dir)


def test_init_type_error_first_arg(repository_dir):
    with pytest.raises(TypeError):
        Certificate(0, 'cloudflare', repository_dir)


def test_init_type_error_second_arg(repository_dir):
    with pytest.raises(TypeError):
        Certificate('my-domain.com', True, repository_dir)


def test_init_type_error_trird_arg(repository_dir):
    with pytest.raises(TypeError):
        Certificate('my-domain.com', 'cloudflare', 0)


@pytest.fixture
def mercurypay_cert(repository_dir):
    return Certificate('mercurypay.io', 'cloudflare', repository_dir)


@pytest.fixture
def get_cert_before_creation(mercurypay_cert):
    mercurypay_cert.rm_domain_conf_file()
    os.system(
        'rm -rf {0}/letsencrypt/renewal/{1}* {2} {0}/letsencrypt/archive/{1}'
        .format(
            repository_dir, mercurypay_cert.domain, mercurypay_cert.live_dir
        )
    )
    return mercurypay_cert


def test_cert_exists_before_create(tmp_path, get_cert_before_creation):
    assert get_cert_before_creation.exists() == False


def test_is_close_to_expire_before_create(tmp_path, get_cert_before_creation):
    with pytest.raises(FileNotFoundError):
        get_cert_before_creation.is_close_to_expire()

# parei aqui. Este teste não funciona
def test_create(tmp_path, get_cert_before_creation):
    get_cert_before_creation.create()
    assert get_cert_before_creation.is_close_to_expire() == False

# def test_is_close_to_expire_300_days_left():
#     assert mercurypay_cert.is_close_to_expire(limit_in_days=300) == True

# def test_cert_exists_after_create():
#     assert mercurypay_cert.exists() == True
