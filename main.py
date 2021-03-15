import os

from classes.Certificate import Certificate

certificate = Certificate("mercurypay.io", "souza")
repository_dir = os.path.dirname(os.path.realpath(__file__))
print(certificate.exists(repository_dir))


# from OpenSSL import crypto
# import datetime
# my_file = crypto.load_certificate(crypto.FILETYPE_PEM, open("letsencrypt/live/mercurypay.io/cert.pem", "r").read())
# my_file.get_notAfter()
# str_time = my_file.get_notAfter().decode('ascii')
# cert_time = datetime.datetime.strptime(str_time, "%Y%m%d%H%M%SZ")

# result = cert_time - datetime.datetime.now() 
# print(result.days)