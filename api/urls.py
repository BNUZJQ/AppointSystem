from django.conf.urls import url, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'classroom', views.ClassroomViewSet)
router.register(r'account', views.AccountViewSet)
router.register(r'appointment', views.AppointmentViewSet)
urlpatterns = (
    url(r'^', include(router.urls)),
)
