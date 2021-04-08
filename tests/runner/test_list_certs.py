import os
import pytest
from sslautomation import AutomationListCerts, Domains
from sslautomation.runner import main
from helpers import ROOT_DIR, CSV_FILE, domains, local_cert


def test_main_list_certs(domains, capsys):
    sys_argv = ['runner.py', '--list-certs']
    main(sys_argv)
    output = capsys.readouterr()
    assert len(output.out.splitlines()) == len(domains)
    assert 'meusucesso.com' in output.out
    assert 'wiseup.com' in output.out
    

def test_list_certs_csv_head_only(capsys):
    os.system("echo 'secret,domain,IP,domain_manager' > {}".format(CSV_FILE))
    domains = Domains(CSV_FILE)
    AutomationListCerts(domains).list_certs()
    output = capsys.readouterr()
    assert len(output.out.splitlines()) == 0
    
    
def test_main_missing_flag():
    with pytest.raises(ValueError):
        sys_argv = ['runner.py']
        main(sys_argv)
        
        
def test_main_wrong_flag():
    with pytest.raises(ValueError):
        sys_argv = ['runner.py', '--anyflag']
        main(sys_argv)
    
    
def test_main_extra_flag():
    with pytest.raises(ValueError):
        sys_argv = ['runner.py', '--list-certs', '--anyflag']
        main(sys_argv)
