from datetime import datetime
from OpenSSL import crypto


class Certificate:
            
    def get_expiry_date(self, cert):
        cert_pem = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
        cert_string_time = cert_pem.get_notAfter().decode('ascii')
        expiry_date = datetime.strptime(cert_string_time, "%Y%m%d%H%M%SZ")
        return expiry_date
    
    def is_close_to_expiring(self, cert, limit_in_days=7):
        expiry_date = self.get_expiry_date()
        time_left = expiry_date - datetime.now()
        return time_left.days < limit_in_days
