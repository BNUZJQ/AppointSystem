from __future__ import unicode_literals

from django.db import models


class ClassroomStatus:
    available = 0
    unavailable = 1
    repairing = 2


CLASSROOM_STATUS_CHOICES = (
    (ClassroomStatus.available, 'available'),
    (ClassroomStatus.unavailable, 'unavailable'),
    (ClassroomStatus.repairing, 'repairing')
)


# Create your models here.
class Classroom(models.Model):
    name = models.SlugField(max_length=255, unique=True)
    status = models.IntegerField(choices=CLASSROOM_STATUS_CHOICES, default=ClassroomStatus.available)
    location = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name
