import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from account.models import Account
from account.serializer import AccountSerializer
from appointment.models import Appointment
from appointment.serializer import AppointmentSerializer
from classroom.models import Classroom
from classroom.serializer import ClassroomSerializer


class ClassroomViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Classroom.objects.all()
        serializer = ClassroomSerializer(queryset, many=True)
        return Response({"size": len(queryset), "data": JSONRenderer().render(serializer.data)})

    def retrieve(self, request, pk=None):
        if not Classroom.objects.filter(name=pk).exists():
            return Response({"message": "Not Found"}, status=404)
        user = request.user
        today = datetime.date.today()
        endday = today + datetime.timedelta(28)
        classroom = Classroom.objects.get(name=pk)
        appointments = classroom.appointment_set.filter(date__gte=today, date__lte=endday)
        # my_appointments = appointments.filter(custom__user=User.objects.get(id=user.id))
        # serialize the queryset
        appointments = AppointmentSerializer(appointments, many=True)
        # my_appointments = AppointmentSerializer(my_appointments, many=True)
        return Response({"success": True,
                         "appointments": JSONRenderer().render(appointments.data),
                         # "my_appointments": JSONRenderer().render(my_appointments.data)
                         },
                        status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        if not Classroom.objects.filter(name=pk).exists():
            return Response({"message": "Not Found"}, status=404)
        appointment = AppointmentSerializer(request.POST)
        if appointment.is_valid():
            return Response(status=201)
        return Response(status=400)

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
