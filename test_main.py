from main import main
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
{:20} - Expiry date: {}
{:20} - Expiry date: {}
{:20} - Expiry date: {}
{:20} - Expiry date: {}
{:20} - Expiry date: {}
{:20} - Expiry date: {}
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







    # criar test passando mais de um argumento
    # criar testes passando mais de um paramentro para a função man
