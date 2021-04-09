import ssl
from sslautomation import Certificate


class WebCert(Certificate):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.web_cert = self.__get_cert()
        
    def __get_cert(self):
        try:
            cert = ssl.get_server_certificate((self.ip, 443))
            return cert
        except Exception as e:
            if type(e).__name__ == 'ConnectionRefusedError' or 'TimeoutError':
                raise ConnectionRefusedError("ERROR: connection failed")
            
    def get_expiry_date(self):
        return super().get_expiry_date(self.web_cert)
    
    def is_close_to_expiring(self, limit_in_days=7):
        return super().is_close_to_expiring(self.web_cert, limit_in_days=7)
