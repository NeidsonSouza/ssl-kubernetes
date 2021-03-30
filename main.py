import sys
from functions.functions import raise_error
from functions.functions import list_certs
from functions.functions import upgrade_repository_certs


def main(flag):
    if len(flag) != 2:
        raise_error()
    elif flag[1] == '--list-certs':
        list_certs()
    elif flag[1] == '--upgrade-repository-certs':
        upgrade_repository_certs()
    elif flag[1] == '--upgrade-certs-prod':
        pass
    else:
        raise_error()


if __name__ == '__main__':
    main(sys.argv)
