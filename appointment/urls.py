from django.conf.urls import url

from appointment.views import index
from appointment.views import myappointment
from appointment.views import post_appointment
from appointment.views import ShowLove

urlpatterns = [
    url(r'^index/$', index),
    url(r'^post_appointment/$', post_appointment),
    url(r'^myappointment/$', myappointment)
]
