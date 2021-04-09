import os
import pytest
import shutil
from sslautomation import Domains, LocalCert

ROOT_DIR = os.getenv('ROOT_DIR')
CSV_FILE = '{}/data/domains.csv'.format(ROOT_DIR)


@pytest.fixture
def domains():
    os.system(
        """\
echo 'secret,domain,IP,domain_manager
xxx,meusucesso.com,34.120.42.5,cloudflare
xxx,wiseup.com,34.95.76.197,cloudflare
' > {}""".format(CSV_FILE)
    )
    return Domains(CSV_FILE)


@pytest.fixture
def local_cert():
    local_cert = LocalCert('wiserpv.com', 'cloudflare')
    archive_dir = '{}/letsencrypt/archive/{}'.format(
        ROOT_DIR, local_cert.domain
    )
    renewal_dir = '{}/letsencrypt/renewal'.format(ROOT_DIR)
    tmp_dir = '/tmp/letsencrypt/{}'.format(local_cert.domain)
    for file_dir in [archive_dir, local_cert.dir, renewal_dir, tmp_dir]:
        if os.path.exists(file_dir): shutil.rmtree(file_dir)
    return local_cert
