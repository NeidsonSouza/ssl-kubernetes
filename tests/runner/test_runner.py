import pytest
from sslautomation.runner import main


def test_main():
    sys_argv = ['runner.py', '--list-certs']
    main(sys_argv)
    
    
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
        sys_argv = ['runner.py', '--list-certs', 'anyflag']
        main(sys_argv)
