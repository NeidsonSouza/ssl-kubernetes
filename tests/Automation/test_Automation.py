import os
import pytest
import shutil
from sslautomation import Automation
from sslautomation import Domains
from sslautomation import LocalCert

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
        if os.path.exists(file_dir):
            shutil.rmtree(file_dir)
    return local_cert


def test_list_certs(domains, capsys):
    Automation(domains).list_certs()
    output = capsys.readouterr()
    assert len(output.out.splitlines()) == len(domains)
    assert 'meusucesso.com' in output.out
    assert 'wiseup.com' in output.out


def test_domains_csv_head_only(capsys):
    os.system("echo 'secret,domain,IP,domain_manager' > {}".format(CSV_FILE))
    domains = Domains(CSV_FILE)
    Automation(domains).list_certs()
    output = capsys.readouterr()
    assert len(output.out.splitlines()) == 0


def test_upgrade_repository_certs_if_not_exists(local_cert):
    create_domains_csv(domain="wiserpv.com", ip='34.95.76.197')
    assert local_cert.exists() == False
    Automation(Domains(CSV_FILE)).upgrade_repository_certs()
    assert local_cert.exists() == True
    

def create_domains_csv(domain, ip):
    domain_manager = "cloudflare"
    os.system("""\
echo 'secret,domain,IP,domain_manager
xxx,{},{},{}
' > {}""".format(domain, ip, domain_manager, CSV_FILE))
    

def test_upgrade_repository_certs_if_not_expiring(local_cert):
    create_domains_csv(domain="wiserpv.com", ip='1.1.1.1')
    assert local_cert.exists() == False
    Automation(Domains(CSV_FILE)).upgrade_repository_certs()
    assert local_cert.exists() == False
    
    
def test_upgrade_repository_certs_raise_error(local_cert):
    create_domains_csv(domain="xxxxxx.com", ip='34.95.76.197')
    assert local_cert.exists() == False
    with pytest.raises(FileNotFoundError):
        Automation(Domains(CSV_FILE)).upgrade_repository_certs()
