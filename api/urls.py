from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'classroom/(?P<classroom>[-\w]+)', views.ClassroomViewSet, base_name="classroom")
router.register(r'account', views.AccountViewSet)
router.register(r'appointment', views.AppointmentViewSet)
urlpatterns = (
    url(r'^', include(router.urls)),
)
