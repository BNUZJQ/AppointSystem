# coding=utf-8
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from account.models import Account
from classroom.models import Classroom


class TIME:
    HOUR8 = 8
    HOUR9 = 9
    HOUR10 = 10
    HOUR11 = 11
    HOUR12 = 12
    HOUR13 = 13
    HOUR14 = 14
    HOUR15 = 15
    HOUR16 = 16
    HOUR17 = 17
    HOUR18 = 18
    HOUR19 = 19
    HOUR20 = 20
    HOUR21 = 21
    HOUR22 = 22
    HOUR23 = 23


TIME_CHOICE = (
    (TIME.HOUR8, 8),
    (TIME.HOUR9, 9),
    (TIME.HOUR10, 10),
    (TIME.HOUR11, 11),
    (TIME.HOUR12, 12),
    (TIME.HOUR13, 13),
    (TIME.HOUR14, 14),
    (TIME.HOUR15, 15),
    (TIME.HOUR16, 16),
    (TIME.HOUR17, 17),
    (TIME.HOUR18, 18),
    (TIME.HOUR19, 19),
    (TIME.HOUR20, 20),
    (TIME.HOUR21, 21),
    (TIME.HOUR22, 22),
    (TIME.HOUR23, 23),
)


class STATUS:
    waiting = 0  # 未到时间
    opened = 1  # 门已打开
    empty = 2  # 钥匙已被取走
    finished = 3  # 钥匙已还
    canceled = 4  # 预约已取消


STATUS_CHOICE = (
    (STATUS.waiting, '未到预约时间'),
    (STATUS.opened, '柜门已打开'),
    (STATUS.empty, '已取走钥匙'),
    (STATUS.finished, '钥匙已还'),
    (STATUS.canceled, '预约已取消')
)


# Create your models here.
class Appointment(models.Model):
    start = models.IntegerField(choices=TIME_CHOICE, blank=False)
    end = models.IntegerField(choices=TIME_CHOICE, blank=False)
    classroom = models.ForeignKey(Classroom, blank=False)
    custom = models.ForeignKey(Account, blank=False)
    date = models.DateField(blank=False)
    reason = models.CharField(max_length=1000, blank=False)
    desk = models.BooleanField(default=False)
    multimedia = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICE, default=STATUS.waiting)
    boss = models.CharField(max_length=100, blank=False)
    director = models.CharField(max_length=100, blank=True)
    director_phone = models.CharField(max_length=11, blank=True)

    class Meta:
        ordering = ('-date', 'start')
        unique_together = (("custom", "classroom", "date", "start", "status"), ("custom", "classroom", "date", "end", "status"))

    def __unicode__(self):
        return u'{}, {}, {}, from {}h. to {}h.'.format(self.classroom.name, self.custom.user.username, self.date,
                                                       self.start, self.end)

    def __str__(self):
        return u'{}, {}, {}, from {}h. to {}h.'.format(self.classroom.name, self.custom.user.username, self.date,
                                                       self.start, self.end)

    def save(self, *args, **kwargs):
        today = date.today()
        if self.date.__lt__(today):
            raise ValidationError("date can NOT before today")
        if self.start > self.end:
            raise ValidationError("end can NOT before than start")
        appointments = Appointment.objects.filter(classroom=self.classroom, date__exact=self.date)
        for appoint in appointments:
            if appoint.start < self.start < appoint.end:
                raise ValidationError("start time unvalid!")
            if appoint.start < self.end < appoint.end:
                raise ValidationError("end time unvalid!")
        if (self.director == "" and self.director_phone != "") or (self.director != "" and self.director_phone == ""):
            raise ValidationError("director & dicrector_phone should both exist or noexist")
        super(Appointment, self).save(*args, **kwargs)
