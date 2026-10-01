from rest_framework import serializers
from .models import ReliefTeacher

class ReliefTeacherSerializer (serializers.ModelSerializer):
    class Meta:
        model = ReliefTeacher
        fields = ["id", "name", "contact_number"]