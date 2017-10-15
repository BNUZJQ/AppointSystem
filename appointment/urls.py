from django.conf.urls import url
from appointment.views import main_appoint
from appointment.views import post_appointment
from appointment.views import choose_classroom

urlpatterns = [
    url(r'^main_appointment', main_appoint),
    url(r'^choose_classroom', choose_classroom),
    url(r'^post_appointment', post_appointment)
]
