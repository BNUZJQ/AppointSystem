from django.conf.urls import url

from account.views import login, home, forget, change_info, personal_info

urlpatterns = [
    url(r'^$', login, name='login'),
    url(r'^home/', home, name='home'),
    url(r'^forget/', forget),
    url(r'^change_info/', change_info),
    url(r'^personal_info/', personal_info),
]
