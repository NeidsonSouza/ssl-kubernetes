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



# sys_argv = ['main.py', '--list-certs']

#     main(sys_argv)
#     captured = capsys.readouterr()
#     assert captured.out == expected

# def main(flag):
#     if len(flag) != 2:
#         raise_error()
#     elif flag[1] == '--list-certs':
#         list_certs()
#     elif flag[1] == '--upgrade-repository-certs':
#         upgrade_repository_certs()
#     elif flag[1] == '--upgrade-certs-prod':
#         pass
#     else:
#         raise_error()


# if __name__ == '__main__':
#     main(sys.argv)