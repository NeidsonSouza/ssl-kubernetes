import os
import sys
from .AutomationListCerts import AutomationListCerts
from .AutomationUpgradeCerts import AutomationUpgradeCerts
from .AutomationUpgradeProxy import AutomationUpgradeProxy
from .Domains import Domains
from .Repository import Repository

ROOT_DIR = os.getenv('ROOT_DIR')
CSV_FILE = '{}/data/domains.csv'.format(ROOT_DIR)
domains = Domains(CSV_FILE)
user = 'monitorssl'
password = 'jYsEmt2S9ktyQehhShPz'

def main():
    repo = Repository(user, password)
    repo.clone()
    repo.create_symlink()
    AutomationListCerts(domains).list_certs()
    AutomationUpgradeCerts(domains).upgrade_repository_certs()
    repo.push()
    AutomationUpgradeProxy(domains).upgrade_proxy()
