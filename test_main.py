from collections import namedtuple
import os
import pytest

from functions.functions import get_cert_before_creation
from classes.Certificate import Certificate
from main import get_domains_as_class
from main import create_certs_if_expired_or_inexistent
from main import get_domains_that_fail
from main import get_email_message


@pytest.fixture
def get_class_domain():
    return namedtuple('Domain', ['name', 'owner'])


def test_get_domains_as_class(get_class_domain):
    os.system('echo  "wiserpv.com=cloudflare\ntest.com=aws" > domains')
    Domain = get_class_domain

    actual = get_domains_as_class()
    expected = [Domain('wiserpv.com', 'cloudflare'), Domain('test.com', 'aws')]
    assert expected == actual


@pytest.fixture
def cert_before_creation():
    cert = Certificate('wiserpv.com', 'cloudflare')
    return get_cert_before_creation(cert)


def test_create_certs_if_expired_or_inexistent(cert_before_creation, get_class_domain):
    Domain = get_class_domain
    domains = [Domain('wiserpv.com', 'cloudflare')]
    create_certs_if_expired_or_inexistent(domains)
    assert cert_before_creation.exists() == True


def test_get_domains_that_fail_empty(cert_before_creation, get_class_domain):
    cert_before_creation.create()
    Domain = get_class_domain
    domains = [Domain('wiserpv.com', 'cloudflare')]
    actual = get_domains_that_fail(domains)
    expected = []
    assert expected == actual


def test_get_domains_that_fail_not_empty(cert_before_creation, get_class_domain):
    Domain = get_class_domain
    domains = [Domain('wiserpv.com', 'cloudflare')]
    actual = get_domains_that_fail(domains)
    expected = ['wiserpv.com']
    assert expected == actual


def test_get_email_message_not_empty():
    message = get_email_message(['wiserpv.com'])
    assert isinstance(message, str)
    assert len(message) != 0


def test_get_email_message_empty():
    message = get_email_message([])
    assert message == None
