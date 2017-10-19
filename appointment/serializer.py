from rest_framework import serializers

from appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    custom = serializers.StringRelatedField()

    class Meta:
        model = Appointment
        fields = '__all__'
