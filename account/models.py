# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class ROLE:
    Student = 'Student'
    Teacher = 'Teacher'
    Admin = 'Admin'
    Blacklist = 'Blacklist'


ROLE_CHOICE = (
    (ROLE.Student, 'Student'),
    (ROLE.Teacher, 'Teacher'),
    (ROLE.Admin, 'Admin'),
    (ROLE.Blacklist, 'Blacklist')
)


class GENDER:
    Male = 'Male'
    Female = 'Female'


GENDER_CHOICE = (
    (GENDER.Male, 'Male'),
    (GENDER.Female, 'Female')
)


class MAJOR:
    EE = "电子"
    CS = "计算机"
    CST = "计算机师范"


MAJOR_CHOICE = (
    (MAJOR.EE, "电子"),
    (MAJOR.CS, "计算机"),
    (MAJOR.CST, "计算机师范")
)


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default=ROLE.Student)
    major = models.CharField(max_length=10, choices=MAJOR_CHOICE, default=MAJOR.EE)
    student_id = models.CharField(max_length=12, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default=GENDER.Male)
    email = models.EmailField(blank=False)
    telephone = models.CharField(max_length=11, blank=True)
    question = models.CharField(max_length=100, blank=True)
    answer = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '{},{}'.format(self.user.username, self.role)
