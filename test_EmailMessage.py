from classes.EmailMessage import EmailMessage
import pytest


def test_init():
    domains = [2, '', 'meudominio.com', 'mydomain.com']
    expected = ['meudominio.com', 'mydomain.com']
    assert EmailMessage(domains).domains == expected


def test_init_empty_list():
    with pytest.raises(ValueError):
        EmailMessage([])


def test_create_email_message():
    desired_message = """\
From: {}
To: {}
Subject: {}

Dominios que apresentaram falha ao gerar o certificado.
Favor verificar detalhes de log no pipeline.

- neidson.com
- souza.com
""".format(
        'dev.work.py@gmail.com', 'neidson.souza@wisereducacao.com', "Some Subject"
    )

    email = EmailMessage(['neidson.com', 'souza.com'])
    message = email.create_email_message(
        'dev.work.py@gmail.com',
        ['neidson.souza@wisereducacao.com'],
        "Some Subject"
    )

    assert message == desired_message
