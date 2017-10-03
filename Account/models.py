from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class ROLE:
    Student = 'Student'
    Teacher = 'Teacher'
    Admin = 'Admin'


ROLE_CHOICE = (
    (ROLE.Student, 'Student'),
    (ROLE.Teacher, 'Teacher'),
    (ROLE.Admin, 'Admin')
)


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default=0)

    def __unicode__(self):
        return self.user.username
