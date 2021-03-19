import os
import sys
from classes.Certificate import Certificate
from classes.GmailAccount import GmailAccount
from classes.File import File
from classes.EmailMessage import EmailMessage

# SERVER = 'https://acme-v02.api.letsencrypt.org/directory' # Production server
SERVER = 'https://acme-staging-v02.api.letsencrypt.org/directory'  # Staging server
REPOSITORY_DIR = os.path.dirname(os.path.realpath(__file__))

domains_file = File('domains')
domains = domains_file.get_content_as_list()

domains_fails = []
should_commit = False
for domain in domains:
    certificate = Certificate(domain.name, domain.owner, REPOSITORY_DIR)
    if certificate.exists():
        if certificate.is_close_to_expire():
            certificate.create(SERVER)
    else:
        certificate.create(SERVER)
        should_commit = True
    if certificate.is_close_to_expire():
        domains_fails.append(domain.name)

if should_commit:
    os.system('git add *.pem')
    os.system("git commit -m'[skip ci] Adding certs'")
    os.system("git push")

if len(domains_fails) > 0:
    sent_from = 'infra.edtech@wisereducacao.com'
    to = File('emails').read_file()
    subject = "[WARNING] Falha ao gerar certificados"
    email = EmailMessage(domains_fails)
    message = email.create_email_message(sent_from, to, subject)

    print(message)
    gmail_password = sys.argv[1]
    gmail_account = GmailAccount(
        'infra.edtech@wisereducacao.com', gmail_password)
    gmail_account.server.sendmail(sent_from, to, message)
    gmail_account.server.close()
