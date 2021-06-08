import os
from datetime import datetime
from .LocalCert import LocalCert
from .WebCert import WebCert

class AutomationListCerts:
    def __init__(self, domains):
        self.domains = domains
        
    def list_certs(self):
        if len(self.domains) > 0:
            return self.__get_domain_and_dates()
            
    def __get_domain_and_dates(self):
        domain_list = []
        for domain in self.domains:
            web_cert = WebCert(domain['secret'])
            domain_list.append(
                {
                    'domain': domain['domain'],
                    'expiry_date': web_cert.get_expiry_date().isoformat(),
                    '5_days_or_less_to_expiry': web_cert.is_close_to_expiring(
                        limit_in_days=5
                    ),
                    'is_expired': web_cert.get_expiry_date() < datetime.now()
                }
            )
        return domain_list
