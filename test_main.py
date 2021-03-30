from main import main
from classes.Certificate import Certificate
from functions.functions import get_cert_before_creation
import os
import pytest


def test_main(capsys):
    os.system(
        """\
echo 'numberone.com.br,34.120.103.130,cloudflare
meusucesso.com,34.120.42.5,cloudflare
wiseup.com,34.95.76.197,cloudflare
powerhouse.pro,34.120.69.210,cloudflare
wiseupcorp.com,35.186.198.149,cloudflare
buzzclub.com.br,34.107.249.226,cloudflare' > domains
"""
    )
    expected = """\
{:20} -> Expiry date: {}
{:20} -> Expiry date: {}
{:20} -> Expiry date: {}
{:20} -> Expiry date: {}
{:20} -> Expiry date: {}
{:20} -> Expiry date: {}
""".format(
        'powerhouse.pro', 'November 26 2019 - 21:15:02',
        'wiseup.com', 'April 06 2020 - 03:12:36',
        'meusucesso.com', 'April 12 2020 - 17:21:13',
        'numberone.com.br', 'May 31 2020 - 01:41:45',
        'buzzclub.com.br', 'November 09 2020 - 19:48:18',
        'wiseupcorp.com', 'November 23 2020 - 20:16:34',
    )
    sys_argv = ['main.py', '--list-certs']

    main(sys_argv)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_more_flags_raise_error():
    sys_argv = ['main.py', '--list-certs', '--any-flag']
    with pytest.raises(ValueError):
        main(sys_argv)


def test_more_than_one_arg_main():
    sys_argv = ['main.py', '--list-certs']
    with pytest.raises(TypeError):
        main(sys_argv, 0)


@pytest.fixture
def cert_before_creation():
    cert = Certificate('wiserpv.com', 'cloudflare')
    return get_cert_before_creation(cert)


def test_upgrade_repository_certs(cert_before_creation):
    # Creating fake data
    domain = "wiserpv.com"
    ip = "34.95.76.197"
    owner = "cloudflare"
    os.system("echo '{},{},{}' > domains".format(domain, ip, owner))
    sys_argv = ['main.py', '--upgrade-repository-certs']
    main(sys_argv)
    assert cert_before_creation.exists() == True
    assert cert_before_creation.is_close_to_expire() == False

# testar domains thar fail