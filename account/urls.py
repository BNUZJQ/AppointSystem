from django.conf.urls import url
from account.views import login, home, complete_info, forget, change_info


urlpatterns = [
    url(r'^$', login, name='login'),
    url(r'^home/', home, name='home'),
    url(r'^complete_info/', complete_info),
    url(r'^forget/', forget),
    url(r'^change_info/', change_info),
]
