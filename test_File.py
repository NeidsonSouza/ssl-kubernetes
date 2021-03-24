from classes.File import File
import pytest
import os


def test_init_type_error():
    with pytest.raises(TypeError):
        File([])


def test_init_empty_str():
    with pytest.raises(ValueError):
        File('')


def test_get_data_from_file():
    os.system(
        'echo  "teste-email@wisereducacao.com\ntest@gmail.com" > test_emails'
    )
    email_file = File('test_emails')
    emails = email_file.get_data_from_file()
    desired_emails = ['teste-email@wisereducacao.com', 'test@gmail.com']
    assert emails == desired_emails


def test_get_data_from_empty_file():
    os.system('> test_emails')
    with pytest.raises(TypeError):
        File('test_emails').get_data_from_file()


def test_get_content_as_list_of_class():
    os.system(
        'echo  "wiserpv.com=cloudflare\nmercurypay.io=aws" > test_domains'
    )
    domain_file = File('test_domains')
    domains = domain_file.get_content_as_list_of_class()
    assert domains[0].name == 'wiserpv.com'
    assert domains[0].owner == 'cloudflare'
    assert domains[1].name == 'mercurypay.io'
    assert domains[1].owner == 'aws'


def test_get_content_as_list_of_class_empty_file():
    os.system('> test_domains')
    with pytest.raises(TypeError):
        File('test_domains').get_content_as_list_of_class()
