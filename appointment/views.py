# coding=utf-8
import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from account.decorator import login_required
from account.models import Account
from appointment.models import Appointment
from appointment.serializer import AppointmentSerializer
from classroom.models import Classroom


@require_POST
@login_required
@csrf_exempt
def choose_classroom(request):
    user = request.user
    classroom_choice = request.POST.get('classroom', None)
    if classroom_choice is None:
        return JsonResponse({"success": False}, status=status.HTTP_400_BAD_REQUEST)
    if not Classroom.objects.filter(name=classroom_choice).exists():
        return JsonResponse({"success": False}, status=status.HTTP_404_NOT_FOUND)
    today = datetime.date.today()
    endday = today + datetime.timedelta(28)
    classroom = Classroom.objects.get(name=classroom_choice)
    appointments = classroom.appointment_set.filter(date__gte=today, date__lte=endday)
    my_appointments = appointments.filter(custom__user=User.objects.get(id=user.id))

    # serialize the queryset
    appointments = AppointmentSerializer(appointments, many=True)
    my_appointments = AppointmentSerializer(my_appointments, many=True)
    return JsonResponse({"success": True,
                         "appointments": JSONRenderer().render(appointments.data),
                         "my_appointments": JSONRenderer().render(my_appointments.data)
                         },
                        status=status.HTTP_200_OK)


@login_required
def main_appoint(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'main_appointment.html', locals())


@require_POST
@login_required
def post_appointment(request):
    user = request.user
    if request.method == 'POST':
        duration_choice = request.POST.get('duration', '')
        data_choice = request.POST.get('date', '')
        reason_reason = request.POST.get('reason', '')
        classroom_choice = request.POST.get('classroom', '')
        appointment = Appointment()
        appointment.duration = duration_choice
        appointment.classroom = Classroom.objects.get(name=classroom_choice)
        appointment.custom = Account.objects.get(user=request.user)
        appointment.date = data_choice
        appointment.reason = reason_reason
        appointment.save()
        return render(request, 'main_appointment.html', locals())
