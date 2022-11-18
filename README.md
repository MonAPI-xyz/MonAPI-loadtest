# MonAPI load testing tools

## Scenario 1 (seed_user.py & locustfile.py)
First scenario is a load testing scenario using locust. It will try to hit API backend endpoint as much as it can.

Configure number of user in config.json

Each user will have:
- 10 standard API monitor
- 5 API monitor with assertions
- 5 API monitor with previous step API monitor (1 depth)

### How to run
1. Prepare empty database on django application
2. Run migration on django by running command `python manage.py migrate`
3. Run django application server
4. Configure endpoint and user_account on `config.json`
5. Run `python seed_user.py` to create account
6. Run locust by running command `locust`
7. Run load test by openning locust ui on port `8089`

## Scenario 2 (monitor_stress_test.py)
Second scenario is stress test the system with as much API monitor the system can handle.

Configure number of user in prompt of monitor_stress_test.py
Configure the api monitor multiplier (x) in prompt of monitor_stress_test.py

Each user will have:
- 10*x standard API monitor
- 5*x API monitor with assertions
- 5*x API monitor with previous step API monitor (1 depth)

### How to run
1. Prepare empty database on django application
2. Run migration on django by running command `python manage.py migrate`
3. Run django application server
5. Run `python monitor_stress_test.py` to generate api monitor
6. Monitor the system metrics in 5 - 15 minutes to see if system is stable and can handle API monitor as expected
