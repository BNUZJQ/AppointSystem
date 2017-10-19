import json

from testing.testcase import TestCase


class ApiTests(TestCase):
    def setUp(self):
        self.bxy = self.createUser('BXY', "123456789")
        self.classroom1 = self.createClassroom("500")
        self.classroom2 = self.createClassroom("400A")
        self.url = "/api/classroom/"

    def test_list(self):
        response = self.client.get(self.url, decode=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['size'], 2)
        data = json.loads(response.data['data'])
        self.assertEqual(data[0]['name'], self.classroom1.name)

    def test_retrieve(self):
        self.createAppointment(self.bxy, self.classroom1)
        response = self.client.get(self.url + self.classroom1.name + "/", decode=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        data = json.loads(response.data['appointments'])
        self.assertEqual(len(data), 1)
        # get a wrong name
        response = self.client.get(self.url + "/" + self.classroom1.name + "12", decode=False)
        self.assertEqual(response.status_code, 404)
