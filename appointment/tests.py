from testing.testcase import TestCase


# Create your tests here.
class AppointmentTests(TestCase):
    def setUp(self):
        self.bxy = self.createUser('BXY', "123456789")
        self.classroom = self.createClassroom("500")

    def test_choose_classroom(self):
        with self.logged_in_user(self.bxy):
            response = self.client.post("/choose_classroom", data={"classroom": self.classroom.name}, decode=False)
            self.assertEqual(response.status_code, 200)
            # post with no data
            response = self.client.post("/choose_classroom", data={}, decode=False)
            self.assertEqual(response.status_code, 400)
            # post with wrong name
            response = self.client.post("/choose_classroom", data={"classroom": "123"}, decode=False)
            self.assertEqual(response.status_code, 404)
        # without login
        response = self.client.post("/choose_classroom", data={"classroom": self.classroom.name}, decode=False)
        self.assertEqual(response.status_code, 302)
