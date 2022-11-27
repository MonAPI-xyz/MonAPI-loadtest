from locust import HttpUser, task
import random
import csv

from common.utils import read_config

config = read_config()

class MonAPILoadTestUser(HttpUser):
    user_account = {}
    api_monitor_id = []
    header = {}
    error_log_id = None

    @task
    def getInviteToken(self):
        self.client.get("invite-member/token/", json={
            'key': "invalid-key"
        }, headers=self.header)

    @task
    def createNewTeam(self):
        self.client.post("/team-management/", json={
            'name': "team-name",
            'description': "team-description",
            'logo': None,
        }, headers=self.header)

    @task
    def editTeam(self):
        resp = self.client.get("/auth/current_team/", headers=self.header)
        resp_current_team = resp.json()
        
        self.client.put(f"/team-management/{resp_current_team['id']}/", json={
            'description': "team-description",
            'logo': None,
        }, headers=self.header)        

    @task
    def login(self):
        self.client.post("/auth/login/", json={
            'email': self.user_account['email'],
            'password': self.user_account['password'],
        })
        
    @task
    def current_team(self):
        resp = self.client.get("/auth/current_team/", headers=self.header)
        resp_current_team = resp.json()
        
        self.client.post("/auth/change_team/", json={
            'id': resp_current_team['id']
        }, headers=self.header)
    
    @task
    def get_available_team(self):
        self.client.get("/auth/available_team", headers=self.header)
        
    # Potential slow query
    @task
    def view_list_api_monitor(self):
        self.client.get('/monitor/', headers=self.header)
    
    @task
    def view_detail_api_monitor(self):
        monitor_id = random.choice(self.api_monitor_id)
        self.client.get(f'/monitor/{monitor_id}/?range=30MIN', headers=self.header)
    
    @task
    def create_and_delete_api_monitor(self):
        resp = self.client.post(f"/monitor/", json={
            "name": f"Test API Create",
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
        }, headers=self.header)
        
        api_monitor = resp.json()
        
        self.client.delete(f"/monitor/{api_monitor['id']}/", headers=self.header)
    
    @task
    def update_api_monitor(self):
        monitor_id = random.choice(self.api_monitor_id)
        self.client.put(f"/monitor/{monitor_id}/", json={
            "name": f"Test API Update",
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
        }, headers=self.header)
    
    @task
    def view_api_monitor_stats(self):
        self.client.get('/monitor/stats/', headers=self.header)
    
    @task
    def view_list_error_logs(self):
        resp = self.client.get('/error-logs/', headers=self.header)
        error_logs = resp.json()
        
        if len(error_logs['results']) > 0:
            self.error_log_id = error_logs['results'][0]['id']
        
    @task
    def view_detail_error_logs(self):
        if self.error_log_id != None:
            self.client.get(f'/error-logs/{self.error_log_id}/', headers=self.header)
    
    @task
    def get_current_config(self):
        self.client.get('/alerts/config/', headers=self.header)
    
    @task
    def update_current_config(self):
        self.client.post('/alerts/config/', json={
            "is_slack_active": False,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": False,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": False,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "is_email_active": False,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": True,
            "email_use_ssl": True
        }, headers=self.header)
    
        
    def on_start(self):
        # Read user mock
        with open('MOCK_USER.csv', newline='') as csv_file:
            reader = csv.reader(csv_file)
            users = []
            
            for idx, row in enumerate(reader):
                if idx >= config['user_count']:
                    break
                
                users.append({
                    'email': row[0],
                    'password': row[1],
                })
                
            self.user_account = random.choice(users)
        
        # Login to account
        response = self.client.post("/login/", json={
            'email': self.user_account['email'],
            'password': self.user_account['password'],
        })
        
        access_token = response.json()['token']
        self.header = {'Authorization': f"Token {access_token}"}
        
        prev_step_id = None
        
        # Standard API Monitor
        for i in range(10):
            resp = self.client.post(f"/monitor/", json={
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
            }, headers=self.header)
            
            api_monitor = resp.json()
            prev_step_id = api_monitor['id']
            self.api_monitor_id.append(api_monitor['id'])
        
        # API Monitor with assertions
        for i in range(5):
            resp = self.client.post(f"/monitor/", json={
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
            }, headers=self.header)
            
            api_monitor = resp.json()
            self.api_monitor_id.append(api_monitor['id'])
            
        # API Monitor with previous step
        for i in range(5):
            resp = self.client.post(f"/monitor/", json={
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
            }, headers=self.header)
            
            api_monitor = resp.json()
            self.api_monitor_id.append(api_monitor['id'])
        
        