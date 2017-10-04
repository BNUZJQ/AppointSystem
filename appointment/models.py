from __future__ import unicode_literals

from account.models import Account
from classroom.models import Classroom
from django.db import models

TIME_CHOICE = (
    (0, '0:00-1:00'),
    (1, '1:00-2:00')
)


# Create your models here.
class Appointment(models.Model):
    duration = models.IntegerField(choices=TIME_CHOICE, blank=False)
    classroom = models.OneToOneField(Classroom, blank=False)
    custom = models.OneToOneField(Account, blank=False)

    def __unicode__(self):
        return u'{},{},{}'.format(self.classroom.name, self.duration, self.custom.user.username)
