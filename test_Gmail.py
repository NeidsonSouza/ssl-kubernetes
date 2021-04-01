from classes.Gmail import Gmail
import pytest


def test_init():
    with pytest.raises(TypeError):
        Gmail(True, 'gmail_password')


def test_init_type_error():
    gemail = Gmail('oi@gmail.com', 'password')
