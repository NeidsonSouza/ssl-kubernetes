import os
import sys
from classes.Certificate import Certificate
from classes.GmailAccount import GmailAccount
from classes.File import File
from classes.EmailMessage import EmailMessage
from dotenv import load_dotenv

load_dotenv()
os.environ['APP_ROOT_DIR'] = os.path.dirname(os.path.realpath(__file__))
os.environ['LETSENCRYPT_DIR'] = os.environ.get('APP_ROOT_DIR') + '/letsencrypt/'
os.chdir(os.environ.get('APP_ROOT_DIR'))

domains_file = File('domains')
domains = domains_file.get_content_as_list()

domains_fails = []
should_commit = False
for domain in domains:
    certificate = Certificate(domain.name, domain.owner, REPOSITORY_DIR)
    if certificate.exists():
        if certificate.is_close_to_expire():
            certificate.create()
    else:
        certificate.create()
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
    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    gmail_account = GmailAccount(
        'infra.edtech@wisereducacao.com', GMAIL_PASSWORD
        )
    gmail_account.server.sendmail(sent_from, to, message)
    gmail_account.server.close()
