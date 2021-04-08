import os
from .LocalCert import LocalCert
from .WebCert import WebCert

class AutomationListCerts:
    def __init__(self, domains):
        self.domains = domains
        
    def list_certs(self):
        if len(self.domains) > 0:
            self.__print_certs()
    
    def __print_certs(self):
        domain_and_date = self.__get_domain_and_date()
        domain_and_date.sort(key=lambda x: x['expiry_date'])
        self.__print(domain_and_date)
            
    def __get_domain_and_date(self):
        return [{
            'domain': domain['domain'],
            'expiry_date': WebCert(domain['IP']).get_expiry_date() 
        } for domain in self.domains]

    def __print(self, domain_and_date):
        for domain in domain_and_date:
            print('{:20} -> Expiry date: {}'.format(
                domain['domain'],
                domain['expiry_date'].strftime("%B %d %Y - %H:%M:%S")
            ))
