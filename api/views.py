from rest_framework import viewsets
from account.models import Account
from account.serializer import AccountSerializer
from appointment.models import Appointment
from appointment.serializer import AppointmentSerializer
from classroom.models import Classroom
from classroom.serializer import ClassroomSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
