import os
import sys
from .Automation import Automation
from .Domains import Domains

def raise_error():
    raise ValueError(
        ""\
        "Flags available:"\
        ""\
        "--list-certs: only list certs and their expiry dates"\
        "--upgrade-repository-certs: upgrade certs only in repository (not in production)"\
        "--upgrade-certs-prod: upgrade certs in production (BE CAREFULL !!!)"\
        ""
    )


def main(flag):
    if len(flag) != 2:
        raise_error()
    if flag[1] == '--list-certs':
        ROOT_DIR = os.getenv('ROOT_DIR')
        scv_file = '{}/data/domains.csv'.format(ROOT_DIR)
        automation = Automation(Domains(scv_file))
        automation.list_certs()
    else:
        raise_error()
