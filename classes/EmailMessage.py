class EmailMessage:

    def __init__(self, domains):
        self.domains = self.__clean_list(domains)
        if len(self.domains) == 0:
            raise ValueError('ERROR: list of domains cannot be empty')

    def __clean_list(self, domains):
        clean_list = [
            domain for domain in domains
            if isinstance(domain, str) and len(domain) != 0
        ]
        return clean_list

    def create_email_message(self, sent_from, to, subject):
        if len(self.domains) > 0:
            body = """
Dominios que apresentaram falha ao gerar o certificado.
Favor verificar detalhes de log no pipeline.

"""
            for domain in self.domains:
                body += "- " + domain + "\n"

        message = """\
From: {}
To: {}
Subject: {}
{}""".format(sent_from, ", ".join(to), subject, body)

        return message
