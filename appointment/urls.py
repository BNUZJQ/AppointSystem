from django.conf.urls import url

from appointment.views import main_appoint
from appointment.views import post_appointment

urlpatterns = [
    url(r'^main_appointment/$', main_appoint),
    url(r'^post_appointment/$', post_appointment)
]
