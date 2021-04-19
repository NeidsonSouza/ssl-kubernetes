from sslautomation import main
import os

if __name__ == '__main__':
    # os.environ['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))
    print('Actual directory: ' + os.environ['ROOT_DIR'])
    main()
