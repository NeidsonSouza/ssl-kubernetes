import os
from classes.Certificate import Certificate
from classes.File import File

# SERVER = 'https://acme-v02.api.letsencrypt.org/directory' # Production server
SERVER = 'https://acme-staging-v02.api.letsencrypt.org/directory' # Staging server
REPOSITORY_DIR = os.path.dirname(os.path.realpath(__file__))

domains_file = File('domains')
domains = domains_file.get_content_as_list()

for domain in domains:
    certificate = Certificate(domain.name)
    if certificate.exists():
        if certificate.is_close_to_expire(limit_in_days=7):
            certificate.create(SERVER)
    else:
        certificate.create(SERVER)
    if certificate.is_close_to_expire(SERVER):
        pass
        # send_email
