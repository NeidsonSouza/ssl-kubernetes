import os
from OpenSSL import crypto
from datetime import datetime

class Certificate:
    def __init__(self, domain, domain_manager, repository_dir):
        self.domain = self.__set_attribute(domain)
        self.domain_manager = self.__set_attribute(domain_manager)
        self.repository_dir = self.__set_attribute(repository_dir)
        self.cert_dir = '{}/letsencrypt/live/{}/'.format(
            self.repository_dir,
            self.domain
            )

    
    def __set_attribute(self, attribute):
        if not isinstance(attribute, str):
            warning_phase = "ERROR: '{}' should be a string"
            self.__raise_error(TypeError, warning_phase, attribute)
        elif len(attribute) == 0:
            warning_phase = "ERROR: '{}' shouldn't have length equal zero"
            self.__raise_error(ValueError, warning_phase, attribute)
        else:
            return attribute


    def __raise_error(self, error_function, warning_phase, key_word):
        raise error_function(warning_phase.format(key_word))


    def exists(self):
        pem_files = [
            'cert.pem', 'chain.pem', 'fullchain.pem', 'privkey.pem'
            ]
        return self.__all_pem_files_exist(self.cert_dir, pem_files)

    
    def __all_pem_files_exist(self, cert_dir, pem_files):
        pem_files_flag = [
            os.path.exists(cert_dir + '/' + each_file)
            for each_file in pem_files
            ]
        return all(pem_files_flag)

    
    def is_close_to_expire(self, limit_in_days=7):
        cert_full_path = self.cert_dir + 'cert.pem'
        cert_pem = crypto.load_certificate(
            crypto.FILETYPE_PEM,
            open(cert_full_path, 'r').read()
            )
        cert_pem_days_left = self.__get_how_many_days_left(cert_pem)
        return cert_pem_days_left < limit_in_days


    def __get_how_many_days_left(self, cert_pem):
        cert_string_time = cert_pem.get_notAfter().decode('ascii')
        cert_datetime = datetime.strptime(cert_string_time, "%Y%m%d%H%M%SZ")
        result = cert_datetime - datetime.now()
        return result.days


    def create(self, letsencrypt_server):
        self.rm_domain_conf_file()
        output = os.system('bash {}/wildcard_cloudflare.sh {} {}'.format(
            self.repository_dir,
            self.domain,
            letsencrypt_server
            )
            )


    def rm_domain_conf_file(self):
        conf_file = 'rm {}/letsencrypt/renewal/{}.conf'.format(
            self.repository_dir, self.domain
        )
        if os.path.exists(conf_file):
            os.system(conf_file)