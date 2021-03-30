import os
from classes.File import File
from classes.Webapp import Webapp
from classes.Certificate import Certificate


def upgrade_repository_certs():
    domains = File('domains').get_content_as_list_of_class()
    for domain in domains:
        web_cert = Webapp(domain.name, domain.ip, domain.owner)
        local_cert = Certificate(domain.name, domain.owner)
        if web_cert.is_close_to_expire():
            if not local_cert.exists():
                local_cert.create()
            elif local_cert.is_close_to_expire():
                local_cert.create()


def get_cert_before_creation(cert):
    def rm_files(files_to_be_removed):
        for filename in files_to_be_removed:
            if os.path.exists(filename):
                os.system('rm -rf {}'.format(filename))

    archive_dir = 'letsencrypt/archive/{}'.format(cert.domain)
    conf_file = 'letsencrypt/renewal/{}.conf'.format(cert.domain)
    files_to_be_removed = [cert.live_dir, archive_dir, conf_file]
    rm_files(files_to_be_removed)
    return cert


def raise_error():
    raise ValueError(
        """

Flags available:

--list-certs: only list certs and their expiry dates
--upgrade-repository-certs: upgrade certs only in repository (not in production)
--upgrade-certs-prod: upgrade certs in production (BE CAREFULL !!!)
"""
    )


def list_certs():
    domains = File('domains').get_content_as_list_of_class()
    list_domain_date = [
        (
            domain.name,
            Webapp(domain.name, domain.ip, domain.owner).get_expiry_date()
        )
        for domain in domains
    ]
    list_domain_date.sort(key=lambda x: x[1])
    for domain in list_domain_date:
        print(
            '{:20} -> Expiry date: {}'.format(
                domain[0], domain[1].strftime("%B %d %Y - %H:%M:%S")
            )
        )
