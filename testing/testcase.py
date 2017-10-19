import datetime
from contextlib import contextmanager

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import caches
from django.test import TestCase as DjangoTestCase

from account.models import Account
from appointment.models import Appointment
from classroom.models import Classroom
from testing.client import Client


class TestCase(DjangoTestCase):
    client_class = Client

    def clearCache(self):
        for cache_name in settings.CACHES:
            caches[cache_name].clear()

    def get_password(self, username):
        return username + '2014'

    def createUser(self, username, email=None, is_staff=False, is_superuser=False):
        user = User.objects.create(username=username, is_staff=is_staff, is_superuser=is_superuser, email=email)
        user.set_password(self.get_password(username))
        user.save()
        return user

    def createClassroom(self, name):
        classroom = Classroom.objects.create(name=name)
        classroom.save()
        return classroom

    def createAppointment(self, user, classroom, start=1, end=2, reason="Test"):
        account = Account.objects.create(user=user)
        account.save()
        appointment = Appointment.objects.create(custom=account, classroom=classroom, date=datetime.datetime.today(),
                                                 start=start, end=end, reason=reason)
        appointment.save()
        return appointment

    @contextmanager
    def logged_in_user(self, user):
        self.log_in_user(user)
        yield
        self.log_out_user()

    def log_in_user(self, user):
        success = self.client.login(username=user.username,
                                    password=self.get_password(user.username))
        self.assertTrue(success)
        self.active_user = user

    def log_out_user(self):
        self.client.logout()
        self.active_user = None
