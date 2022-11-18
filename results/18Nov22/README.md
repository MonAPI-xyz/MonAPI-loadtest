# Load testing 18 November 2022

## Server specification
- CPU 2 cores
- Memory 4 GB
- Storage 50 GB

## Scenario 1 (locust)

Load testing result shown average RPS around 15 - 20 RPS on average of all endpoints in MonAPI

Slowest endpoint of all endpoint is /monitor/ (propably because this endpoint makes ~24*monitor count db query for each request)

## Scenario 2 (API Monitor stress test)

We test using 5 user with configuration on 20, 100, 200, 300, 600, 1000, 2000 monitor for each user

| No | User Count | Monitor per user | Total monitor on system  | Average CPU |
|---|---|---|---|---|
| 1 | 5 | 20 | 100 | 10%
| 2 | 5 | 100 | 500 | 34%
| 3 | 5 | 200 | 1000 | 63%
| 4 | 5 | 300 | 1500 | 70%
| 5 | 5 | 600 | 3000 | 91%
| 6 | 5 | 1000 | 5000 | 93%
| 7 | 5 | 2000 | 10000 | 100%

Based on the graph on CPU usage, we can say that the system can handle 1500 API monitors easily without any issue. When the API monitor reach 5000 and 10000, the system is still faily usable but often feels slow because the cron impact. 