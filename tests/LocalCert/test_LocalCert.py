import os
import pytest
import shutil
from datetime import datetime, timedelta
from sslautomation import LocalCert

ROOT_DIR = os.getenv('ROOT_DIR')


@pytest.fixture
def local_cert():
    return cleanup_local_cert()

def cleanup_local_cert():
    local_cert = LocalCert('wiserpv.com', 'cloudflare')
    archive_dir = '{}/letsencrypt/archive/{}'.format(
        ROOT_DIR, local_cert.domain
    )
    renewal_dir = '{}/letsencrypt/renewal'.format(ROOT_DIR)
    tmp_dir = '/tmp/letsencrypt/{}'.format(local_cert.domain)
    for file_dir in [archive_dir, local_cert.dir, renewal_dir, tmp_dir]:
        if os.path.exists(file_dir):
            shutil.rmtree(file_dir)
    return local_cert
    

def test_exist_create_expire_date(local_cert, capsys):
    assert local_cert.exists() == False
    tst_expiry_date_before_create(local_cert)
    tst_is_close_to_expiring_before_create(local_cert)
    local_cert.create()
    captured = capsys.readouterr()
    assert os.getenv('SERVER') in captured.out
    assert local_cert.exists() == True
    tst_expiry_date_after_create(local_cert)
    tst_is_close_to_expiring_after_create(local_cert)
    cleanup_local_cert()
    local_cert.create()


def tst_expiry_date_before_create(cert):
    with pytest.raises(FileNotFoundError):
        cert.get_expiry_date()


def tst_is_close_to_expiring_before_create(cert):
    with pytest.raises(FileNotFoundError):
        cert.is_close_to_expiring()
        

def tst_expiry_date_after_create(cert):
    actual = datetime.strftime(cert.get_expiry_date(), "%Y-%m-%d")
    expected = datetime.strftime(
        datetime.now() + timedelta(days=90), "%Y-%m-%d"
    )
    assert actual == expected

        
def tst_is_close_to_expiring_after_create(cert):
    assert cert.is_close_to_expiring() == False
    