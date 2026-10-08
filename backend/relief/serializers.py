from rest_framework import serializers
from .models import ReliefTeacher, TeacherAvailability, Subject, Level
class TeacherAvailabilitySerializer (serializers.ModelSerializer):
    class Meta:
        model = TeacherAvailability
        fields = ["day_of_week","start_time","end_time"]


class ReliefTeacherSerializer (serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField (
        many=True,
        slug_field="name",
        queryset=Subject.objects.all()
    )#get the related subject and represent it as a string
    levels = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Level.objects.all()
    )
    availability = TeacherAvailabilitySerializer (many=True)
   
    class Meta:
        model = ReliefTeacher
        fields = ["id", "name", "contact_number","subjects","levels","availability"]