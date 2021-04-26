from sslautomation import main
import os

if __name__ == '__main__':
    # print('Actual directory: ' + os.environ['ROOT_DIR'])
    # main()
    
    
    
    import json
    data = {
        'array':
            [
                {
                    'runtime': '2012-04-23T18:25:43.511Z',
                    'domain': 'meusucesso.com',
                    'expiry_date:': '2021-06-23T18:25:43.511Z',
                    'was_updated': True
                },
                {
                    'runtime': '2012-04-23T18:25:43.511Z',
                    'domain': 'wiseup.com',
                    'expiry_date:': '2020-05-11T17:19:43.511Z',
                    'was_updated': False
                },
                {
                    'runtime': '2012-04-23T18:25:43.511Z',
                    'domain': 'powerhouse.pro',
                    'expiry_date:': '2022-11-02T15:25:08.511Z',
                    'was_updated': True
                }
            ]
    }
    
    # print(data)
    # print("")
    app_json = json.dumps(data)
    print(app_json)
