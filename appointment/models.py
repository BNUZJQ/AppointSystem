from __future__ import unicode_literals

from account.models import Account
from classroom.models import Classroom
from django.db import models

TIME_CHOICE = (
    (0, '8:00-8:30'),
    (1, '8:30-9:00'),
    (2, '9:00-9:30'),
    (3, '9:30-10:00'),
    (4, '10:00-10:30'),
    (5, '10:30-11:00'),
    (6, '11:00-11:30'),
    (7, '11:30-12:00'),
    (8, '12:00-12:30'),
    (9, '12:30-13:00'),
    (10, '13:30-14:00'),
    (11, '14:00-14:30'),
    (12, '14:30-15:00'),
    (13, '15:00-15:30'),
    (14, '15:30-16:00'),
    (15, '16:00-16:30'),
    (16, '16:30-17:00'),
    (17, '17:30-18:00'),
    (18, '18:00-18:30'),
    (19, '18:30-19:00'),
    (20, '19:00-19:30'),
    (21, '19:30-20:00'),
    (22, '20:00-20:30'),
    (23, '20:30-21:00'),
    (24, '21:00-21:30'),
    (25, '21:30-22:00'),
    (26, '22:00-23:00')
)


# Create your models here.
class Appointment(models.Model):
    duration = models.IntegerField(choices=TIME_CHOICE, blank=False)
    classroom = models.OneToOneField(Classroom, blank=False)
    custom = models.OneToOneField(Account, blank=False)
    date = models.DateTimeField(blank=False)
    reason = models.CharField(max_length=1000, blank=False)

    def __unicode__(self):
        return u'{},{},{}'.format(self.classroom.name, self.duration, self.custom.user.username, self.data, self.reason)
