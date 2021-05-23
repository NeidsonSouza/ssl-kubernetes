import os
from .Certificate import Certificate


class LocalCert(Certificate):    
    def __init__(self, domain, domain_manager):
        super().__init__()
        self.ROOT_DIR = os.getenv('ROOT_DIR')
        self.domain = domain
        self.domain_manager = domain_manager
        self.dir = '{}/letsencrypt/live/{}'.format(self.ROOT_DIR, self.domain)
        self.cert_pem_dir = self.dir + '/cert.pem'
    
    
    def exists(self):
        pem_files = [
            'cert.pem', 'chain.pem', 'fullchain.pem', 'privkey.pem'
        ]
        return all(
            os.path.exists(self.dir + '/' + file_name)
            for file_name in pem_files
        )
    
    
    def create(self):
        os.makedirs('/tmp/letsencrypt/{}'.format(self.domain))
        print(os.getenv('SERVER'))
        if self.domain_manager == 'cloudflare':
            print('{} hosted on Cloudflare'.format(self.domain))
            os.system(
                """certbot certonly \
                --non-interactive \
                --email dominios@wisereducacao.com \
                --server $SERVER \
                --dns-cloudflare \
                --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
                --dns-cloudflare-propagation-seconds 120 \
                --agree-tos \
                -d {0},*.{0}""".format(self.domain)
            )
        elif self.domain_manager == 'aws':
            print('{} hosted on AWS'.format(self.domain))
            os.system(
                """certbot certonly \
                --non-interactive \
                --email dominios@wisereducacao.com \
                --server $SERVER \
                --dns-route53 \
                --agree-tos \
                -d {0},*.{0}""".format(self.domain)
            )
        else:
            raise ValueError("ERROR: {} not found in rules. It shoud be 'aws' or 'cloudflare'")
        
    
    def get_expiry_date(self):
        return super().get_expiry_date(self.__get_cert())
    
    
    def __get_cert(self):
        return open(self.cert_pem_dir, 'r').read()
    
    
    def is_close_to_expiring(self, limit_in_days=7):
        return super().is_close_to_expiring(
            self.__get_cert(), limit_in_days=limit_in_days
        )