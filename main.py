import sys
from classes.File import File
from classes.Webapp import Webapp


def main(flag):
    if len(flag) != 2:
        raise_error()
    elif flag[1] == '--list-certs':
        list_certs()
    elif flag[1] == '--upgrade-certs-repository':
        pass
    elif flag[1] == '--upgrade-certs-prod':
        pass
    else:
        raise_error()


def raise_error():
    raise ValueError(
        """

Flags available:

--list-certs: only list certs and their expiry dates
--upgrade-certs-repository: upgrade certs only in repository (not in production)
--upgrade-certs-prod: upgrade certs in production (BE CAREFULL !!!)
"""
    )


def list_certs():
    domains = File('domains').get_content_as_list_of_class()
    list_domain_date = [
        (
            domain.name,
            Webapp(domain.name, domain.ip, domain.owner).get_expiry_date()
        )
        for domain in domains
    ]
    list_domain_date.sort(key=lambda x: x[1])
    for domain in list_domain_date:
        print(
            '{:20} - Expiry date: {}'.format(
                domain[0], domain[1].strftime("%B %d %Y - %H:%M:%S")
            )
        )


if __name__ == '__main__':
    main(sys.argv)
