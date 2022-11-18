import csv
import requests
import csv

from common.utils import read_config

user_count = int(input("Masukkan jumlah pengguna: "))
multiplier = int(input("Multiplier count: "))
config = read_config()
session = requests.Session() # To use one connection for all requests

with open('MOCK_USER.csv', newline='') as csv_file:
    reader = csv.reader(csv_file)
    
    for idx, row in enumerate(reader):
        if idx >= user_count:
            break
        
        print (f'register account {idx+1}')
        session.post(f"{config['backend_url']}/register/api", json={
            'email': row[0],
            'password': row[1],
            'password2': row[1],
        })
        
        email = row[0]
        password = row[1]

        # Login to account
        print (f'login account {idx+1}')
        response = session.post(f"{config['backend_url']}/login/", json={
            'email': email,
            'password': password,
        })

        access_token = response.json()['token']
        header = {'Authorization': f"Token {access_token}"}

        prev_step_id = None
        
        print (f'create api monitor {idx+1}')
        # Standard API Monitor
        for i in range(10*multiplier):
            resp = session.post(f"{config['backend_url']}/monitor/", json={
                "name": f"Test API {i}",
                "method": "GET",
                "url": "https://jsonplaceholder.typicode.com/posts/1",
                "schedule": "1MIN",
                "body_type": "EMPTY",
                "previous_step_id": "",
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": "",
                "assertion_type": "DISABLED",
                "assertion_value": "",
                "is_assert_json_schema_only": False,
                "exclude_keys": []
            }, headers=header)
            
            api_monitor = resp.json()
            prev_step_id = api_monitor['id']

        # API Monitor with assertions
        for i in range(5*multiplier):
            resp = session.post(f"{config['backend_url']}/monitor/", json={
                "name": f"Test API {i}",
                "method": "GET",
                "url": "https://jsonplaceholder.typicode.com/posts/1",
                "schedule": "1MIN",
                "body_type": "EMPTY",
                "previous_step_id": "",
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": "",
                "assertion_type": "JSON",
                "assertion_value": '{\
                    "userId": 1,\
                    "id": 1,\
                    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",\
                    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"\
                }',
                "is_assert_json_schema_only": False,
                "exclude_keys": []
            }, headers=header)
            
            
        # API Monitor with previous step
        for i in range(5*multiplier):
            resp = session.post(f"{config['backend_url']}/monitor/", json={
                "name": f"Test API {i}",
                "method": "GET",
                "url": "https://jsonplaceholder.typicode.com/posts/1",
                "schedule": "1MIN",
                "body_type": "EMPTY",
                "previous_step_id": prev_step_id,
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": "",
                "assertion_type": "DISABLED",
                "assertion_value": "",
                "is_assert_json_schema_only": False,
                "exclude_keys": []
            }, headers=header)
            

