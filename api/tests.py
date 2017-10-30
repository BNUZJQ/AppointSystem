# coding=utf-8
import datetime

from account.models import ROLE
from appointment.models import Appointment
from testing.testcase import TestCase


class ApiTests(TestCase):
    def setUp(self):
        self.bxy = self.createAccount('BXY', role=ROLE.Student)
        self.zjq = self.createAccount('ZJQ', role=ROLE.Blacklist)
        self.classroom1 = self.createClassroom("500")
        self.classroom2 = self.createClassroom("400A")
        self.url = "/api/classroom/"
        self.today = datetime.date.today()

    def test_list(self):
        self.createAppointment(self.bxy, self.classroom1)
        # without login
        response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
        self.assertEqual(response.status_code, 403)
        # with normal student user
        with self.logged_in_user(self.bxy.user):
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['success'], True)
            self.assertEqual(len(response.data['appointments']), 1)
            # get a wrong name
            response = self.client.get(self.url + "/" + self.classroom1.name + "12", decode=False)
            self.assertEqual(response.status_code, 404)
        # with Blacklist user(ok for list)
        with self.logged_in_user(self.zjq.user):
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['success'], True)
            self.assertEqual(len(response.data['appointments']), 1)
            # test get My appointment
            response = self.client.get(self.url + self.classroom1.name + "/", data={"mine": True}, decode=False)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['success'], True)
            self.assertEqual(len(response.data['appointments']), 0)

    def test_create_without_login(self):
        data = {
            "classroom": self.classroom1.name,
            "start": 8,
            "end": 10,
            "date": str(self.today),
            "reason": "test",
            "boss": "xiqi"
        }
        response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
        self.assertEqual(response.status_code, 403)

    def test_create_with_blacklist_user(self):
        with self.logged_in_user(self.zjq.user):
            data = {
                "classroom": self.classroom1.name,
                "start": 8,
                "end": 10,
                "date": str(self.today),
                "reason": "test",
                "boss": "xiqi"
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 403)

    def test_create_conflict_time(self):
        with self.logged_in_user(self.bxy.user):
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            init_size = response.data['size']
            data = {
                "classroom": self.classroom1.name,
                "start": 8,
                "end": 10,
                "date": str(self.today),
                "reason": "test",
                "boss": "xiqi"
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 201)
            # 检查预约的个数是否增加了
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size + 1)
            # 预约一个冲突的时间
            data = {
                "classroom": self.classroom1.name,
                "start": 9,
                "end": 11,
                "date": str(self.today),
                "reason": "test",
                "boss": '稀奇'
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            # 检查预约的个数是否增加了
            response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size + 1)

    def test_create_other_circumstance(self):
        with self.logged_in_user(self.bxy.user):
            # post with start < end
            data = {
                "classroom": self.classroom1.name,
                "start": "9",
                "end": "8",
                "date": str(self.today),
                "reason": "test",
                "boss": '稀奇'
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('non_field_errors' in response.data, True)

            # post without reason
            data = {
                "classroom": self.classroom1.name,
                "start": "9",
                "end": "10",
                "date": str(self.today),
                "boss": '稀奇'
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('reason' in response.data, True)

            # post without before date
            data = {
                "classroom": self.classroom1.name,
                "start": "9",
                "end": "10",
                "date": str(self.today - datetime.timedelta(1)),
                "reason": "test",
                "boss": '稀奇'
            }
            response = self.client.post(self.url + self.classroom1.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual('non_field_errors' in response.data, True)

    def test_delete(self):
        with self.logged_in_user(self.bxy.user):
            response = self.client.get(self.url + self.classroom2.name + "/", decode=False)
            init_size = response.data['size']
            data = {
                "classroom": self.classroom2.name,
                "start": 8,
                "end": 10,
                "date": str(self.today),
                "reason": "test",
                "boss": '稀奇'
            }
            response = self.client.post(self.url + self.classroom2.name + "/", data=data, decode=False)
            self.assertEqual(response.status_code, 201)
            # 检查预约的个数是否增加了
            response = self.client.get(self.url + self.classroom2.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size + 1)

            # 删除刚刚创建的预约
            id = Appointment.objects.get(classroom=self.classroom2, date=self.today, start=8).id
            # response = self.client.delete(self.url +self.classroom.name + "/" + str(id) + "/", decode=False)
            response = self.client.post(self.url + self.classroom2.name + "/" + str(id) + "/delete_appoint/", decode=False)
            self.assertEqual(response.status_code, 204)
            # 检查预约个数是否减少
            response = self.client.get(self.url + self.classroom2.name + "/", decode=False)
            self.assertEqual(response.data['size'], init_size)

            # 删除一个不存在的appoint
            # response = self.client.delete(self.url + self.classroom2.name + "/" + str(id + 1000) + "/", decode=False)
            response = self.client.post(self.url + self.classroom2.name + "/" + str(id + 1000) + "/delete_appointe/", decode=False)
            self.assertEqual(response.status_code, 404)
