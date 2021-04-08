import os
from .LocalCert import LocalCert
from .WebCert import WebCert

class Automation:
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

    def upgrade_repository_certs(self):
        if len(self.domains) > 0:
            self.__upgrade()
            
    def __upgrade(self):
        certs_created = []
        for domain in self.domains:
            web_cert = WebCert(domain['IP'])
            local_cert = LocalCert(domain['domain'], domain['domain_manager'])
            if web_cert.is_close_to_expiring():
                if not local_cert.exists() or local_cert.is_close_to_expiring():
                    local_cert.create()
                    certs_created.append(local_cert) 
        self.__git_add_commit_push()
        self.__raise_error_if_any_expiring(certs_created)
        
        
    def __git_add_commit_push(self):
        os.system(
        "git add *.pem && git commit -m'[skip ci] Certs added $(date)' && git push"
        )
        pass
    
    def __raise_error_if_any_expiring(self, certs):
        for local_cert in certs:
            if not local_cert.exists():
                raise FileNotFoundError(
                    "ERROR: {} certificate was not created".format(
                        local_cert.domain
                    )
                )
