# MonAPI load testing tools

## How to run
1. Prepare empty database on django application
2. Run migration on django by running command `python manage.py migrate`
3. Run django application server
4. Configure endpoint and user_account on `config.json`
5. Run `python seeddb.py` to create account
6. Run locust by running command `locust`
7. Run load test by openning locust ui on port `8089`
