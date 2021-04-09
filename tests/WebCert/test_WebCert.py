import pytest
import re
from datetime import datetime
from sslautomation import WebCert


@pytest.fixture
def web_cert():
    return WebCert('34.107.249.226')
    
    
def test_get_expiry_date(web_cert):
    str_time = datetime.strftime(web_cert.get_expiry_date(), "%Y-%m-%d")
    is_date_matching = re.search(
        r'^20\d{2}-(0[1-9]|1[0-2])-([0-2]\d|3[0-1])$', str_time
    )
    assert is_date_matching


def test_is_close_to_expiring(web_cert):
    web_cert.is_close_to_expiring()


def test_get_expiry_date_wrong_ip():
    with pytest.raises(ConnectionRefusedError):
        web_cert = WebCert('6.6.6.6')
