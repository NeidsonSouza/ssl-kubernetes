import re
import OpenSSL
import ssl
from datetime import datetime

from classes.Certificate import Certificate


class Webapp:
    def __init__(self, domain, ip, owner):
        self.domain = self.validate_as_string(domain)
        self.ip = self.validate_as_ip(ip)
        self.owner = self.validate_as_owner(owner)
        self.local_cert = Certificate(self.domain, self.owner)
        self.webcert = ssl.get_server_certificate((self.ip, 443))

    def validate_as_string(self, string):
        if not isinstance(string, str):
            warning_phase = "ERROR: '{}' should be a string"
            raise TypeError(warning_phase.format(string))
        elif len(string) == 0:
            warning_phase = "ERROR: '{}' shouldn't have length equal zero"
            raise ValueError()(warning_phase.format(string))
        else:
            return string

    def validate_as_owner(self, owner):
        if owner != 'cloudflare' and 'aws':
            raise ValueError('ERROR: {} should be "cloudflare" or "aws"')
        else:
            return owner

    def validate_as_ip(self, ip):
        if not isinstance(ip, str):
            warning_phase = "ERROR: '{}' should be a string"
            raise TypeError(warning_phase.format(ip))
        else:
            regex = re.compile(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$')
            ip_after_parse = regex.match(ip)
            if ip_after_parse:
                return ip
            else:
                warning_phase = "ERROR: '{}' should be an IP"
                raise ValueError(warning_phase.format(ip))
            
    def get_expiry_date(self):
        return self.local_cert.get_expiry_date(self.webcert)

    def is_close_to_expire(self, limit_in_days=7):
        return self.local_cert.is_close_to_expire(
            limit_in_days=limit_in_days, cert=self.webcert
            )

    def create_cert(self):
        self.local_cert.create()