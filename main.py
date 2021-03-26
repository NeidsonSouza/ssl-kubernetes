import sys
from classes.File import File


def main(flag):
    if len(sys.argv) != 1:
        raise_error()
    elif flag == '--list-certs':
        list_certs()
    elif flag == '--upgrade-certs-repository':
        pass
    elif flag == '--upgrade-certs-prod':
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
    domains_file
    #read file
    #for em cada item
        # print cada item em ordem de data (menor para maior)
        
    #     domains_file = File('domains')
    # domains = domains_file.get_content_as_list_of_class()
    # return domains


if __name__ == '__main__':
    main(sys.argv)
