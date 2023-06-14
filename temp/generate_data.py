from faker import Faker
import random


class GenData:
    def __init__(self, count_data):
        self.count_data = count_data
        self.fake = Faker()

    def data_user(self):
        dict_user = {}
        array = []
        for count_user in range(self.count_data):
            dict_user['user_login'] = self.fake.simple_profile()['username'] #self.fake.first_name()
            dict_user['user_password'] = self.fake.password()
            dict_user['email'] = self.fake.email()
            array.append(dict_user.copy())
        return array

    def data_salary(self):
        dict_salary = {}
        array = []
        for count_salary in range(self.count_data):
            dict_salary['salary'] = random.randint(10_000, 200_000)
            dict_salary['date_raising'] = str(self.fake.date_between(start_date='-2y', end_date='today'))
            array.append(dict_salary.copy())
        return array

