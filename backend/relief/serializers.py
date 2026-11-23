from rest_framework import serializers
from .models import ReliefTeacher, TeacherAvailability, Subject, Level, TeacherLevel
class TeacherAvailabilitySerializer (serializers.ModelSerializer):
    class Meta:
        model = TeacherAvailability
        fields = ["day_of_week","start_time","end_time"]

class TeacherLevelSerializer(serializers.ModelSerializer):
    
    level = serializers.SlugRelatedField(
        slug_field="name", #the api will output name field rather than the primary key (id)
        queryset = Level.objects.all() #returns all the levels in the levels table. Objects lets you CRUD with the DB
    )

    subjects = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset = Subject.objects.all(), #returns all the subjects in the subject table
        allow_empty = False
    )

    class Meta:
        model = TeacherLevel
        fields = ["level","subjects"]


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
    teaching_levels = TeacherLevelSerializer(many=True, required=False) #previously read only = true means django will not accept or validate the field. It only returns the field. required=false means it can accept, return and validate data but the data is not required.

    class Meta:
        model = ReliefTeacher
        fields = ["id", "name", "contact_number","subjects","levels","availability","teaching_levels"] #the json object will now return teaching_levels which contain levels and subjects at that level

    def to_representation(self, instance) :
        data = super().to_representation(instance)
        data["subjects"] = list(instance.subjects.values_list("name", flat = True))
        data["levels"] = list(instance.levels.values_list("name", flat = True))

        return data
    
    def update(self, instance, validated_data):
        availability_data = validated_data.pop("availability",None)
        subjects_data = validated_data.pop("subjects",None)
        levels_data = validated_data.pop("levels",None)
        teaching_levels_data = validated_data.pop("teaching_levels", None) #extracts the teaching_levels from validated_data and stores it in teaching_levels_data. Removes teaching_levels from validated_data before super().update() runs.                                                                                                                                                                                                                                                                                                                                 
            


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

                if teaching_levels_data is not None:
                    instance.teaching_levels_data.all().delete()

                    for item in teaching_levels_data:
                        level = item["level"]
                        subjects = item["subjects"]

                        teacher_level = TeacherLevel.objects.create(
                            teacher=instance,
                            level=level
                        )
                        teacher_level.subjects.set(subjects)

        return instance