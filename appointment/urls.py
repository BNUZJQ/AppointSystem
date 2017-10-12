from django.conf.urls import url
from appointment.views import main_appoint

urlpatterns = [
    url(r'^appoint', main_appoint),
]
