import pytest
from classes import Certificate

certificate = Certificate(domain, manager)

def test_is_close_to_expire():
    certificate.is_close_to_expire()