from django.conf.urls import url

from account.views import login, home, forget, personal_info, logout
from appointment.views import index

urlpatterns = [
    url(r'^$', login, name='login'),
    url(r'^login/', login, name='login'),
    url(r'^home/', home, name='home'),
    url(r'^forget/', forget),
    url(r'^personal_info/', personal_info),
    url(r'^index/', index, name='index'),
    url(r'^logout/', logout, name='logout')
]
