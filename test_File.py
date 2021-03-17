from classes.File import File


# Person = namedtuple('Person', ['first_name', 'last_name', 'age'])

# someone = Person('John', 'Smith', '25')

def test_read_file():
    email_file = File('test_emails')
    emails = email_file.read_file()
    desired_emails = ['teste-email@wisereducacao.com', 'test@gmail.com']
    
    assert emails == desired_emails


def test_get_content_as_list():
    domain_file = File('test_domains')
    domains = domain_file.get_content_as_list()
    assert domains[0].name == 'wiserpv.com'
    assert domains[0].owner == 'cloudflare'
    assert domains[1].name == 'mercurypay.io'
    assert domains[1].owner == 'aws'
