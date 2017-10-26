import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from account.models import Account
from account.serializer import AccountSerializer
from appointment.models import Appointment
from appointment.serializer import AppointmentSerializer
from classroom.models import Classroom


class ClassroomViewSet(viewsets.GenericViewSet):
    serializer_class = AppointmentSerializer

    def list(self, request, **kwargs):
        classroom = kwargs['classroom']
        user = request.user
        today = datetime.date.today()
        endday = today + datetime.timedelta(28)
        classroom = Classroom.objects.get(name=classroom)
        appointments = classroom.appointment_set.filter(date__gte=today, date__lte=endday)
        size = len(appointments)
        # serialize the queryset
        appointments = AppointmentSerializer(appointments, many=True)
        # my_appointments = appointments.filter(custom__user=User.objects.get(id=user.id))
        # my_appointments = AppointmentSerializer(my_appointments, many=True)
        return Response({"success": True,
                         "size": size,
                         "appointments": JSONRenderer().render(appointments.data),
                         },
                        status=status.HTTP_200_OK)

    def retrieve(self, request, **kwargs):
        pass

    @csrf_exempt
    def create(self, request, **kwargs):
        classroom = kwargs["classroom"]
        if not Classroom.objects.filter(name=classroom).exists():
            return Response({"message": "Classroom Not Found"}, status=404)
        classroom = Classroom.objects.get(name=classroom)
        appointment = AppointmentSerializer(data=request.POST)
        if appointment.is_valid(raise_exception=True):
            appointment.save(custom=Account.objects.get(user=request.user), classroom=classroom)
            return Response(status=201)
        return Response({"message": appointment.errors}, status=400)

    @detail_route(methods=['post'])
    def check_appointment(self, request):
        account = Account.objects.get(student_id=request.POST.get('student_id'))
        today = datetime.datetime.today()
        appointments = account.appointment_set.filter(date__day=today)
        for appoint in appointments:
            if today.hour == appoint.start - 1:
                result = {"classroom": appoint.classroom.name,
                          "open": True

                          }


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
