from main import list_cert_dates
import os


def test_main():
    os.system(
        """\
echo 'meusucesso.com,34.120.42.5,cloudflare
wiseup.com,34.95.76.197,cloudflare' > file
"""
    )
    expected = """\
{:20} - Expiry date: {}
{:20} - Expiry date: {}
""".format(
        'wiseup.com', 'April 06 2020 - 03:12:36',
        'meusucesso.com', 'April 12 2020 - 03:12:36'
    )
    sys_argv = ['--list-certs']

    main(sys_argv)
    captured = capsys.readouterr()
    assert captured.out == expected







    # criar test passando mais de um argumento
    # criar testes passando mais de um paramentro para a função man
