# coding=utf-8
import json

from testing.testcase import TestCase


class ApiTests(TestCase):
    def setUp(self):
        self.bxy = self.createAccount('BXY', "123456789")
        self.classroom1 = self.createClassroom("500")
        self.classroom2 = self.createClassroom("400A")
        self.url = "/api/classroom/"

    def test_list(self):
        self.createAppointment(self.bxy, self.classroom1)
        response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        data = json.loads(response.data['appointments'])
        self.assertEqual(len(data), 1)
        # get a wrong name
        response = self.client.get(self.url + "/" + self.classroom1.name + "12", decode=False)
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        with self.logged_in_user(self.bxy.user):
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            init_size = response.data['size']
            data = {
                "start": "8",
                "end": "9",
                "date": "2017-10-22",
                "reason": "test",
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 201)
            # 检查预约的个数是否增加了
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size + 1)

            # post with start < end
            data = {
                "start": "9",
                "end": "8",
                "date": "2017-10-22",
                "reason": "test",
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('non_field_errors' in response.data, True)

            # post without reason
            data = {
                "start": "9",
                "end": "8",
                "date": "2017-10-22",
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
