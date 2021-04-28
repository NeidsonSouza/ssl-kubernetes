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
    dates = AutomationListCerts(domains).list_certs()
    AutomationUpgradeCerts(domains).upgrade_repository_certs()
    print(json.dumps(dates))
    # repo.push()
    # AutomationUpgradeProxy(domains).upgrade_proxy()
    
    
    # import json
    # data = {
    #     'array':
    #         [
    #             {
    #                 'domain': 'meusucesso.com',
    #                 'expiry_date': '2021-06-23T18:25:43.511Z',
    #                 '5_days_or_less_to_expiry': True,
    #                 'is_expired': False,
    #                 'was_cert_replaced': True
    #             },
    #             {
    #                 'domain': 'wiseup.com',
    #                 'expiry_date': '2020-05-11T17:19:43.511Z',
    #                 '5_days_or_less_to_expiry': True,
    #                 'is_expired': True,
    #                 'was_cert_replaced': False
    #             },
    #             {
    #                 'domain': 'powerhouse.pro',
    #                 'expiry_date': '2022-11-02T15:25:08.511Z',
    #                 '5_days_or_less_to_expiry': False,
    #                 'is_expired': False,
    #                 'was_cert_replaced': True
    #             }
    #         ]
    # }

    # app_json = json.dumps(data)
    # print(app_json)
