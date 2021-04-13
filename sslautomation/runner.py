import os
import sys
from .AutomationListCerts import AutomationListCerts
from .AutomationUpgradeCerts import AutomationUpgradeCerts
from .AutomationUpgradeProxy import AutomationUpgradeProxy
from .Domains import Domains

ROOT_DIR = os.getenv('ROOT_DIR')
CSV_FILE = '{}/data/domains.csv'.format(ROOT_DIR)
    
def main(flag):
    if len(flag) != 2:
        raise_error()
    elif flag[1] == '--list-certs':
        AutomationListCerts(Domains(CSV_FILE)).list_certs()
    elif flag[1] == '--upgrade-repository-certs':
        AutomationUpgradeCerts(Domains(CSV_FILE)).upgrade_repository_certs()
    elif flag[1] == '--upgrade-proxy-prod':
        AutomationUpgradeProxy(Domains(CSV_FILE)).upgrade_proxy()
    else:
        raise_error()


def raise_error():
    raise ValueError(
        ""\
        "Flags available:"\
        ""\
        "--list-certs: only list certs and their expiry dates"\
        "--upgrade-repository-certs: upgrade certs only in repository (not in production)"\
        "--upgrade-proxy-prod: upgrade certs in production (BE CAREFULL !!!)"\
        ""
    )
