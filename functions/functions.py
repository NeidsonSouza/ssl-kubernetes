import os
from classes.File import File
from classes.Webapp import Webapp
from classes.Certificate import Certificate
from shutil import copyfile


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
    git_add_commit_push()
    raise_error_if_not_created(domains)


def git_add_commit_push():
    os.system(
        "git add *.pem && git commit -m'[skip ci] Adding certs' && git push"
    )


def raise_error_if_not_created(domains):
    for domain in domains:
        if not Certificate(domain.name, domain.owner).exists():
            raise FileNotFoundError(
                "ERROR: the {} certificate was not created".format(domain)
            )


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
--upgrade-certs-gcp: upgrade certs in production (BE CAREFULL !!!)
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


def upgrade_certs_gcp():
    domains = File('domains').get_content_as_list_of_class()
    for domain in domains:
        web_cert = Webapp(domain.name, domain.ip, domain.owner)
        local_cert = Certificate(domain.name, domain.owner)
        if web_cert.is_close_to_expire():
            if not local_cert.exists() or local_cert.is_close_to_expire():
                pass  # raise
            else:
                metadata_dir = 'metadata/{}'.format(local_cert.domain)
                make_dir(metadata_dir, local_cert)
                __update_infra()

def make_dir(metadata_dir, local_cert):
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
        pem_files = [
            'cert.pem', 'chain.pem', 'fullchain.pem', 'privkey.pem'
        ]
        for single_file in pem_files:
            copyfile(
                '{}/{}'.format(local_cert.live_dir, single_file),
                '{}/{}'.format(metadata_dir, single_file)
            )
    
def __update_infra():
    pass