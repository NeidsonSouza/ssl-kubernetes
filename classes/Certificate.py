import os

class Certificate:
    def __init__(self, domain, domain_manager):
        self.domain = self.__set_attribute(domain)
        self.domain_manager = self.__set_attribute(domain_manager)

    
    def __set_attribute(self, attribute):
        if not isinstance(attribute, str):
            warning_phase = "ERROR: '{}' should be a string"
            self.raise_error(TypeError, warning_phase, attribute)
        elif len(attribute) == 0:
            warning_phase = "ERROR: '{}' shouldn't have length equal zero"
            self.raise_error(ValueError, warning_phase, attribute)
        else:
            return attribute


    def raise_error(self, error_function, warning_phase, key_word):
        raise error_function(warning_phase.format(key_word))


    def exists(self, repository_dir):
        cert_path = repository_dir + '/letsencrypt/live/' + self.domain
        pem_files = [
            'cert.pem', 'chain.pem', 'fullchain.pem', 'privkey.pem'
            ]
        return self.__all_pem_files_exist(cert_path, pem_files)

    
    def __all_pem_files_exist(self, cert_path, pem_files):
        pem_files_flag = [
            os.path.exists(cert_path + '/' + each_file)
            for each_file in pem_files
            ]
        return all(pem_files_flag)

    
    def is_close_to_expire(self, days_left=7):
        pass


    def create(self):
        pass
