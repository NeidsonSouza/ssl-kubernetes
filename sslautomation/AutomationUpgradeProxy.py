import os
from .LocalCert import LocalCert
from .WebCert import WebCert

class AutomationUpgradeProxy:
    def __init__(self, domains):
        if len(domains) > 0:
            self.domains = domains
        else:
            print ('WARNING: {}/data/domains.csv empty'.format(os.getenv(
                'ROOT_DIR'
            )))
            exit(0)

    def upgrade_proxy(self):
        print('Checking if any proxy at GKE cluster need to be upgraded...')
        expiring_web_domains = self._get_domain_expired_in_web()
        if len(expiring_web_domains) > 0:
            print('Secrets to be upgraded: {}'.format(
                [domain['secret'] for domain in expiring_web_domains]
            ))
            proxy_to_be_upgraded = self._get_proxy_to_be_upgraded(
                expiring_web_domains
            )
            self._upgrade_each_proxy(proxy_to_be_upgraded)
        else:
            print('No proxy upgraded')
            return [
                {'domain': domain['domain'], 'was_cert_replaced': False}
                for domain in self.domains
            ]
        return self.__get_final_list(proxy_to_be_upgraded)
    
    def __get_final_list(self, proxy_to_be_upgraded):
        replaced_secrets = [domain['secret'] for domain in proxy_to_be_upgraded]
        final_list = []
        for domain in self.domains:
            if domain['secret'] in replaced_secrets:
                final_list.append(
                    {'domain': domain['domain'], 'was_cert_replaced': True}
                )
            else:
                final_list.append(
                    {'domain': domain['domain'], 'was_cert_replaced': False}
                )
        return final_list

    def _get_domain_expired_in_web(self, domains=None):
        if domains == None: domains = self.domains
        expired_web_certs = [
            domain
            for domain in domains
            if WebCert(domain['secret']).is_close_to_expiring()            
        ]
        return expired_web_certs

    def _get_proxy_to_be_upgraded(self, expiring_web_domains):
        proxy_to_be_upgraded = []
        for domain in expiring_web_domains:
            local_cert = LocalCert(domain['domain'], domain['domain_manager'])
            if local_cert.exists() and not local_cert.is_close_to_expiring():
                proxy_to_be_upgraded.append({
                    'local_cert': local_cert,
                    'secret': domain['secret']
                })
        return proxy_to_be_upgraded

    def _upgrade_each_proxy(self, proxy_to_be_upgraded):
        NAMESPACE = 'proxy'
        del_cmd = 'kubectl delete secret {0} --namespace={1}'
        create_cmd = text = 'kubectl create secret tls {0} '\
                             '--namespace={1} '\
                             '--key {2}/privkey.pem '\
                             '--cert {2}/fullchain.pem'
        for proxy in proxy_to_be_upgraded:
            full_del_cmd = del_cmd.format(proxy['secret'], NAMESPACE)
            full_create_cmd = create_cmd.format(
                proxy['secret'], NAMESPACE, proxy['local_cert'].dir
            )
            cmd = '{} && {}'.format(full_del_cmd, full_create_cmd)
            print(cmd)
            if os.popen(cmd).read() == '':
                raise Exception("Command '{}' Didn't work".format(cmd))
