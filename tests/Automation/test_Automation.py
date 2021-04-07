import os
import pytest
from sslautomation import Automation
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


def test_list_certs(domains, capsys):
    automation = Automation(domains)
    automation.list_certs()
    output = capsys.readouterr()
    assert len(output.out.splitlines()) == len(domains)
    assert 'meusucesso.com' in output.out
    assert 'wiseup.com' in output.out


def test_domains_csv_head_only(capsys):
    os.system("echo 'secret,domain,IP,domain_manager' > {}".format(CSV_FILE))
    domains = Domains(CSV_FILE)
    automation = Automation(domains)
    automation.list_certs()
    output = capsys.readouterr()
    assert len(output.out.splitlines()) == 0
