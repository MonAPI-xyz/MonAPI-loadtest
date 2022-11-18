from faker import Faker
import csv

faker = Faker()

# User account generator
# Generates: email and password

with open('MOCK_USER.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    for i in range(1000):
        data = [faker.email(), faker.bothify(text='????????####')]
        writer.writerow(data)
