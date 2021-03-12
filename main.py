import os

from classes.Certificate import Certificate

certificate = Certificate("mercurypay.io", "souza")
repository_dir = os.path.dirname(os.path.realpath(__file__))
print(certificate.exists(repository_dir))