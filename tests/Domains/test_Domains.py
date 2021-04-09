import os
import pytest
from sslautomation import Domains

CSV_FILE = '{}/data/domains.csv'.format(os.getenv('ROOT_DIR'))

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


def test__len__(domains):
    assert len(domains) == 2


def test__getitem__(domains):
    assert domains[0] == {
        'secret': 'xxx',
        'domain': 'meusucesso.com',
        'IP': '34.120.42.5',
        'domain_manager': 'cloudflare'
    }
    assert domains[1] == {
        'secret': 'xxx',
        'domain': 'wiseup.com',
        'IP': '34.95.76.197',
        'domain_manager': 'cloudflare'
    }

def test_empty_domains_csv():
    os.system('> {}'.format(CSV_FILE))
    domains = Domains(CSV_FILE)
    assert len(domains) == 0
    with pytest.raises(IndexError):
        domains[0]
