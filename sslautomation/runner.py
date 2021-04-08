import os
import sys
from .Automation import Automation
from .Domains import Domains


def main(flag):
    automation = get_automation()
    if len(flag) != 2:
        raise_error()
    elif flag[1] == '--list-certs':
        automation.list_certs()
    elif flag[1] == '--upgrade-repository-certs':
        automation.upgrade_repository_certs()
    else:
        raise_error()
        
    
def get_automation():
    ROOT_DIR = os.getenv('ROOT_DIR')
    scv_file = '{}/data/domains.csv'.format(ROOT_DIR)
    return Automation(Domains(scv_file))


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
