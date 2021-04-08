import os
import pytest
from sslautomation import Automation, Domains
from sslautomation.runner import main
from helpers import ROOT_DIR, CSV_FILE, domains, local_cert


def create_domains_csv(domain, ip, secret='xxx'):
    domain_manager = "cloudflare"
    os.system("""\
echo 'secret,domain,IP,domain_manager
{},{},{},{}
' > {}""".format(secret, domain, ip, domain_manager, CSV_FILE))
    
    
def test_upgrade_repository_certs_if_not_expiring(local_cert):
    create_domains_csv(domain="wiserpv.com", ip='1.1.1.1')
    assert local_cert.exists() == False
    domains = Domains(CSV_FILE)
    Automation(domains).upgrade_repository_certs()
    assert local_cert.exists() == False
    
@pytest.mark.xfail
def test_upgrade_repository_certs_if_not_exists(local_cert):
    create_domains_csv(domain="wiserpv.com", ip='34.95.76.197')
    assert local_cert.exists() == False
    domains = Domains(CSV_FILE)
    Automation(domains).upgrade_repository_certs()
    assert local_cert.exists() == True
    
@pytest.mark.xfail
def test_upgrade_repository_certs_raise_error(local_cert):
    create_domains_csv(domain="xxxxxx.com", ip='34.95.76.197')
    assert local_cert.exists() == False
    with pytest.raises(FileNotFoundError):
        Automation(Domains(CSV_FILE)).upgrade_repository_certs()
