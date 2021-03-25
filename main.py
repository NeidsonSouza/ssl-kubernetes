import os
import sys
from classes.Certificate import Certificate
from classes.Gmail import Gmail
from classes.File import File
from classes.EmailMessage import EmailMessage


def get_domains_as_class():
    domains_file = File('domains')
    domains = domains_file.get_content_as_list_of_class()
    return domains


def create_certs_if_expired_or_inexistent(domains):
    global should_commit
    should_commit = False
    for domain in domains:
        cert = Certificate(domain.name, domain.owner)
        if cert.exists():
            if cert.is_close_to_expire():
                cert.create()
        else:
            cert.create()
            should_commit = True


def get_domains_that_fail(domains):
    domains_that_fail = []
    for domain in domains:
        cert = Certificate(domain.name, domain.owner)
        if cert.exists():
            if cert.is_close_to_expire():
                domains_that_fail.append(domain.name)
        else:
            domains_that_fail.append(domain.name)
    return domains_that_fail


def git_push(should_commit):
    if should_commit:
        os.system('git add *.pem')
        os.system("git commit -m'[skip ci] Adding certs'")
        os.system("git push")


def get_email_message(domains_that_fail):
    if len(domains_that_fail) > 0:
        sent_from = 'infra.edtech@wisereducacao.com'
        to = File('emails').get_data_from_file()
        subject = "[WARNING] Falha ao gerar certificados"
        email = EmailMessage(domains_that_fail)
        message = email.create_email_message(sent_from, to, subject)
        print(message)
        return message


def send_email(message):
    if isinstance(message, str):
        GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
        gmail_account = Gmail(
            'infra.edtech@wisereducacao.com', GMAIL_PASSWORD
        )
        sent_from = 'infra.edtech@wisereducacao.com'
        to = File('emails').get_data_from_file()
        gmail_account.server.sendmail(sent_from, to, message)
        gmail_account.server.close()


if __name__ == '__main__':
    domains = get_domains_as_class()
    create_certs_if_expired_or_inexistent(domains)
    domains_that_fail = get_domains_that_fail(domains)
    message = get_email_message(domains_that_fail)
    send_email(message)
    git_push(should_commit)
