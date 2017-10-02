from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICE = (
    (0, 'Student'),
    (1, 'Teacher'),
    (2, 'Admin')
)


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(choices=ROLE_CHOICE, default=0)

    def __unicode__(self):
        return self.user.username
