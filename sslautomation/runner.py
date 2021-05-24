import json
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
    AutomationUpgradeCerts(domains).upgrade_repository_certs()
    repo.push()
    replaced_certs = AutomationUpgradeProxy(domains).upgrade_proxy()
    dates = AutomationListCerts(domains).list_certs()
    join_dict = [
        {**dic_date, **dic_secret}
        for dic_date, dic_secret in zip(dates, replaced_certs)
    ]
    final_dict = {'array': join_dict}
    json_payload = json.dumps(final_dict)
    print(json_payload)
