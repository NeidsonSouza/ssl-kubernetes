from socket import gaierror
import pytest
from classes.Webapp import Webapp


@pytest.fixture()
def webapp():
    domain = 'wiseup.com'
    ip = '34.95.76.197'
    owner = 'cloudflare'
    return Webapp(domain, ip, owner)


def test_init(webapp):
    domain = 'wiseup.com'
    ip = '34.95.76.197'
    owner = 'cloudflare'
    assert webapp.domain == domain
    assert webapp.ip == ip
    assert webapp.owner == owner


def test_init_missing_arg():
    with pytest.raises(TypeError):
        Webapp('wiseup.com')


def test_init_raise_type_error_1nd_arg():
    with pytest.raises(TypeError):
        Webapp(0, '1.1.1.1', 'cloudflare')


def test_init_raise_type_error_2nd_arg_isnt_ip():
    with pytest.raises(ValueError):
        Webapp('wiseup.com', '1.234.5.6.7', 'cloudflare')


def test_init_raise_type_error_2nd_isnt_string():
    with pytest.raises(TypeError):
        Webapp('wiseup.com', True, 'cloudflare')


def test_init_raise_type_error_3nd_arg():
    with pytest.raises(ValueError):
        Webapp('wiseup.com', '1.1.1.1', 0)


def test_cert_is_close_to_expire(webapp):
    assert webapp.is_close_to_expire() == True

def test_create_cert():
    domain = 'wiserpv.com'
    ip = '1.1.1.1'
    owner = 'cloudflare'
    wiserpv_web = Webapp(domain, ip, owner)
    wiserpv_web.create_cert()
    assert wiserpv_web.local_cert.is_close_to_expire() == False
