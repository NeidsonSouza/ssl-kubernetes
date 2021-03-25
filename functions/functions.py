import os


def get_cert_before_creation(cert):
    def rm_files(files_to_be_removed):
        for filename in files_to_be_removed:
            if os.path.exists(filename):
                os.system('rm -rf {}'.format(filename))

    archive_dir = 'letsencrypt/archive/{}'.format(cert.domain)
    conf_file = 'letsencrypt/renewal/{}.conf'.format(cert.domain)
    files_to_be_removed = [cert.live_dir, archive_dir, conf_file]
    rm_files(files_to_be_removed)
    return cert
