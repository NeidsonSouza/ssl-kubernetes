import os
import shutil

class Repository:
    def __init__(self, user, password):
        self.NAME = 'ssl-certificates'
        self.ROOT_DIR = os.getenv('ROOT_DIR')
        self.URL = "https://{}:{}@bitbucket.org/wisereducacao/{}.git".format(
            user,
            password,
            self.NAME
        )

    def clone(self):
        os.system('git clone {}'.format(self.URL))

    def create_symlink(self):
        for folder in ['archive', 'live']:
            src = '{}/ssl-certificates/letsencrypt/{}'.format(
                self.ROOT_DIR, folder
            )
            dst = '{}/letsencrypt/{}'.format(self.ROOT_DIR, folder)
            print('Deleting {}...'.format(dst))
            shutil.rmtree(dst)
            print('Creating symlink: {} -> {}'.format(src, dst))
            os.symlink(src, dst)

    def push(self):
        os.chdir('{}/{}'.format(self.ROOT_DIR, self.NAME))
        self._run_cmd(
            'git config user.email "ssl.certs.gcp@wisereducacao.com"'
        )
        self._run_cmd('git config user.name "GCP SSL Automation"')
        self._run_cmd(
            "git add *.pem && "\
            "git commit -m'[skip ci] Certs added' && "\
            "git push"
        )
        
    def _run_cmd(self, cmd):
        print(cmd)
        return os.system(cmd)
        