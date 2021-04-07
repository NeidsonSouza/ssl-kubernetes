from .LocalCert import LocalCert

class Automation:
    def __init__(self, domains):
        self.domains = domains
        
    def list_certs(self):
        if len(self.domains) > 0:
            self.__print_certs()
    
    def __print_certs(self):
        for domain in self.domains:
            local_cert = LocalCert(domain['domain'], domain['domain_manager'])
            print(
                '{:20} -> Expiry date: {}'.format(
                    domain['domain'],
                    local_cert.get_expiry_date().strftime(
                        "%B %d %Y - %H:%M:%S"
                    )
                )
            )
