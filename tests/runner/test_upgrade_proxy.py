import pytest
import os
import sys
import shutil
from sslautomation import AutomationUpgradeProxy, Domains, LocalCert
from sslautomation.runner import main as principal
from helpers import CSV_FILE, ROOT_DIR

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

def create_domains_csv(domain, ip, secret='xxx'):
    domain_manager = "cloudflare"
    os.system("""\
echo 'secret,domain,IP,domain_manager
{},{},{},{}
' > {}""".format(secret, domain, ip, domain_manager, CSV_FILE))


def test_init():
    os.system("echo 'secret,domain,IP,domain_manager' > {}".format(CSV_FILE))
    domains = Domains(CSV_FILE)
    with pytest.raises(SystemExit):
        AutomationUpgradeProxy(domains)
    print('expected:\nWARNING: /app/data/domains.csv empty')
    

@pytest.mark.xfail
def test_upgrade_proxy_if_expiring():
    create_domains_csv(
        domain="wiserpv.com", ip='34.95.76.197', secret='wiserpv-certificate'
    )
    domains = Domains(CSV_FILE)
    AutomationUpgradeProxy(domains).upgrade_proxy()
    text_del = 'kubectl delete secret wiserpv-certificate --namespace=proxy'
    text_create = 'kubectl create secret tls buzzclub-certificate '\
           '--namespace=proxy '\
           '--key {0}/letsencrypt/live/wiserpv.com/privkey.pem '\
           '--cert {0}/letsencrypt/live/wiserpv.com/fullchain.pem'.format(ROOT_DIR)
    print('expected:\n' + text_del + '\n' + text_create)
    

def test_upgrade_proxy_if_not_expiring():
    create_domains_csv(
        domain="wiserpv.com", ip='1.1.1.1', secret='wiserpv-certificate'
    )
    domains = Domains(CSV_FILE)
    AutomationUpgradeProxy(domains).upgrade_proxy()
    text_del = 'kubectl delete secret wiserpv-certificate --namespace=proxy'
    text_create = 'kubectl create secret tls buzzclub-certificate '\
           '--namespace=proxy '\
           '--key {0}/letsencrypt/live/wiserpv.com/privkey.pem '\
           '--cert {0}/letsencrypt/live/wiserpv.com/fullchain.pem'.format(ROOT_DIR)
    print('Not expected:\n' + text_del + '\n' + text_create)
    

def test_upgrade_proxy_if_local_non_existe():
    local_cert()
    create_domains_csv(
        domain="wiserpv.com", ip='34.95.76.197', secret='wiserpv-certificate'
    )
    domains = Domains(CSV_FILE)
    AutomationUpgradeProxy(domains).upgrade_proxy()
    text_del = 'kubectl delete secret wiserpv-certificate --namespace=proxy'
    text_create = 'kubectl create secret tls buzzclub-certificate '\
           '--namespace=proxy '\
           '--key {0}/letsencrypt/live/wiserpv.com/privkey.pem '\
           '--cert {0}/letsencrypt/live/wiserpv.com/fullchain.pem'.format(ROOT_DIR)
    print('Not expected:\n' + text_del + '\n' + text_create)


def test_main_upgrade_repository_certs():
    local_cert()
    create_domains_csv(domain="wiserpv.com", ip='1.1.1.1')
    sys_argv = ['runner.py', '--upgrade-proxy-prod']
    principal(sys_argv)


def main():
    test_upgrade_proxy_if_expiring()
    test_init()
    test_main_upgrade_repository_certs()
    test_upgrade_proxy_if_not_expiring()
    test_upgrade_proxy_if_local_non_existe()
    

if __name__ == '__main__':
    main()
