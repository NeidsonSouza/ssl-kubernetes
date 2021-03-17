from classes.File import File

def test_read_file():
    email_file = File('test_emails')
    emails = email_file.read_file()
    desired_emails = ['teste-email@wisereducacao.com', 'test@gmail.com']
    
    assert emails == desired_emails