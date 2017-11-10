# coding=utf-8
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from account.models import Account, ROLE
from account.permissions import AccountPermission
from account.serializer import AccountSerializer
from appointment.models import Appointment, STATUS
from appointment.permissions import AppointmentPermission
from appointment.serializer import AppointmentSerializer
from classroom.models import Classroom


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AccountPermission,)

    @list_route(methods=['post'])
    def change_role(self, request):
        if 'username' not in request.POST or 'role' not in request.POST:
            return Response({"message": "you should input student name"}, status=status.HTTP_400_BAD_REQUEST)
        user_account = Account.objects.get(user=request.user)
        stu = get_object_or_404(Account, user__username=request.POST['username'])
        # 如果操作者不是teacher 就403
        if user_account.role != ROLE.Teacher:
            return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)
        if request.POST['role'] == 'Blacklist':
            stu.role = ROLE.Blacklist
        else:
            stu.role = ROLE.Student
        stu.save()
        return Response({"success": True}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['get'])
    def student(self, request):
        queryset = Account.objects.filter(role=ROLE.Student)
        data = queryset.values('user__username', 'gender', 'email', 'telephone', 'student_id')
        return Response({"size": len(queryset), "data": data})

    @list_route(methods=['get'])
    def blacklist(self, request):
        queryset = Account.objects.filter(role=ROLE.Blacklist)
        data = queryset.values('user__username', 'gender', 'email', 'telephone', 'student_id')
        return Response({"size": len(queryset), "data": data})


class AppointmentViewSet(viewsets.GenericViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = (AppointmentPermission,)

    # STATUS为 cancaled的订单信息不会返回
    def list(self, request):
        user = request.user
        today = datetime.date.today()
        endday = today + datetime.timedelta(28)

        appointments = Appointment.objects.all()
        # 根据request.GET的字段来筛选返回数据
        if 'classroom' in request.GET:
            classroom = Classroom.objects.get(name=request.GET['classroom'])
            appointments = classroom.appointment_set
        if 'mine' in request.GET:
            appointments = appointments.filter(custom__user=user)
        if 'previous' in request.GET:
            appointments = appointments.filter(date__lte=today).order_by('-date')
        else:
            appointments = appointments.filter(date__gte=today,
                                               date__lte=endday,
                                               status=STATUS.waiting).distinct().order_by('date', 'start')
        appointments = appointments.values('id',
                                           'classroom',
                                           'reason',
                                           'date',
                                           'start',
                                           'end',
                                           'desk',
                                           'multimedia',
                                           'status',
                                           'custom__user__username',
                                           'custom__telephone')
        size = len(appointments)
        return Response({"success": True,
                         "size": size,
                         "appointments": appointments,
                         },
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        appointment = get_object_or_404(Appointment, id=pk)
        serializer = AppointmentSerializer(appointment)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @csrf_exempt
    def create(self, request):
        classroom = request.POST['classroom']
        if not Classroom.objects.filter(name=classroom).exists():
            return Response({"message": "Classroom Not Found"}, status=404)
        classroom = Classroom.objects.get(name=classroom)
        appointment = AppointmentSerializer(data=request.POST)
        if appointment.is_valid(raise_exception=True):
            appointment.save(custom=Account.objects.get(user=request.user), classroom=classroom)
            return Response(status=201)
        return Response({"message": appointment.errors}, status=400)

    # delete并非真正删除，而是将status置为canceled
    # TODO 解决这里的crsf问题
    # def delete(self, request, pk):
    #     appointment = get_object_or_404(Appointment, id=pk)
    #     appointment.status = STATUS.canceled
    #     appointment.save()
    #     return Response({"message": "cancel this appointment"}, status=status.HTTP_204_NO_CONTENT)

    # 这种写法实际上是不符合REST的规范的
    @csrf_exempt
    @detail_route(methods=['post'])
    def delete_appoint(self, request, pk):

        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = STATUS.canceled
        appointment.save()
        return Response({"message": "cancel this appointment"}, status=status.HTTP_204_NO_CONTENT)
