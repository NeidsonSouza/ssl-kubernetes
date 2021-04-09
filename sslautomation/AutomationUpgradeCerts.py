import os
from .LocalCert import LocalCert
from .WebCert import WebCert

class AutomationUpgradeCerts:
    def __init__(self, domains):
        if len(domains) > 0:
            self.domains = domains
        else:
            print ('WARNING: {}/data/domains.csv empty'.format(os.getenv(
                'ROOT_DIR'
            )))
            exit(0)
            
    def upgrade_repository_certs(self):
        expired_web_domains = self._get_domain_expired_in_web()
        certs_to_be_created = self._get_expiring_or_missing_certs(
            expired_web_domains
        )
        self._create_certs(certs_to_be_created)
        self._git_add_commit_push()
        not_created_domains = self._get_not_created_domains(certs_to_be_created)
        if len(not_created_domains) != 0: self._raise_error(not_created_domains)
        
    def _get_domain_expired_in_web(self):
        expired_web_certs = [
            domain
            for domain in self.domains
            if WebCert(domain['IP']).is_close_to_expiring()            
        ]
        return expired_web_certs
    
    def _get_expiring_or_missing_certs(self, expired_web_domains):
        certs_to_be_created = []
        for domain in expired_web_domains:
            local_cert = LocalCert(domain['domain'], domain['domain_manager'])
            if not local_cert.exists() or local_cert.is_close_to_expiring():
                certs_to_be_created.append(local_cert)
        return certs_to_be_created
        
    def _create_certs(self, certs_to_be_created):
        for cert in certs_to_be_created: cert.create()
    
    def _get_not_created_domains(self, certs_to_be_created):
        return [
            cert.domain for cert in certs_to_be_created if not cert.exists()
        ]
    
    def _git_add_commit_push(self):
        os.system(
            "git add *.pem && "\
            "git commit -m'[skip ci] Certs added $(date)' && "\
            "git push"
        )
        
    def _raise_error(self, not_created_domains):
        raise FileNotFoundError("ERROR: certificates not created:\n{}".format(
                not_created_domains
        ))
