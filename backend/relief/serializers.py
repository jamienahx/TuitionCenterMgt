from rest_framework import serializers
from .models import ReliefTeacher, TeacherAvailability, Subject, Level
class TeacherAvailabilitySerializer (serializers.ModelSerializer):
    class Meta:
        model = TeacherAvailability
        fields = ["day_of_week","start_time","end_time"]


class ReliefTeacherSerializer (serializers.ModelSerializer):
    subjects = serializers.ListField(
        child = serializers.CharField(),
        write_only = True
    )
    levels = serializers.ListField(
        child = serializers.CharField(),
        write_only = True
    )
    availability = TeacherAvailabilitySerializer (many=True, required=False)
   
    class Meta:
        model = ReliefTeacher
        fields = ["id", "name", "contact_number","subjects","levels","availability"]

    def to_representation(self, instance) :
        data = super().to_representation(instance)
        data["subjects"] = list(instance.subjects.values_list("name", flat = True))
        data["levels"] = list(instance.levels.values_list("name", flat = True))

        return data
    
    def update(self, instance, validated_data):
        availability_data = validated_data.pop("availability",None)
        subjects_data = validated_data.pop("subjects",None)
        levels_data = validated_data.pop("levels",None)

        instance = super().update(instance, validated_data)
        if levels_data is not None:
            levels =[]

            for name in levels_data:
                level, created = Level.objects.get_or_create(name=name.strip())
                levels.append(level)
            instance.levels.set(levels)
               
            


        if subjects_data is not None:
            subjects = []

            for name in subjects_data:
                subject, created = Subject.objects.get_or_create(name=name.strip())
                subjects.append(subject)
            
            instance.subjects.set(subjects)
           
          

        if availability_data is not None:
            instance.availability.all().delete()

            for item in availability_data:
                TeacherAvailability.objects.create(
                    teacher=instance,
                    **item
                )

        return instance