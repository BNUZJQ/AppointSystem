from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from Account.api.api import AccountViewSet

router = DefaultRouter()
router.register(r'account', AccountViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
