from rest_framework import serializers
from .models import ReliefTeacher, TeacherAvailability, Subject, Level, TeacherLevel
from django.db import transaction

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
    
    def validate_teaching_levels(self, value): #prevent dupes in teacher_levels because it violates the DB design of having a unique level-subject combi. Models already have it, but this is the validation layer. Value here also speciically refers to the teaching_levels, whereas validated_data typically refers to ALL fields

        seen_levels = set() #a set is a list that doe not contain duplicate values and there is no insertion order

        for item in value:

            level = item["level"] #extract the "levels" part from the dictionary

            if level in seen_levels: #check whether the level already exists
                raise serializers.ValidationError(
                    f"Duplicate teaching level: {level.name}"
            )

            seen_levels.add(level)

        return value

    def to_representation(self, instance) :
        data = super().to_representation(instance)
        data["subjects"] = list(instance.subjects.values_list("name", flat = True))
        data["levels"] = list(instance.levels.values_list("name", flat = True))

        return data
    
    @transaction.atomic # transaction.atomic groups the whole transaction together and ensures that only when all operations  are successful will the DB update. if even one fails, nothing gets updated
    def update(self, instance, validated_data):
        availability_data = validated_data.pop("availability",None)
        subjects_data = validated_data.pop("subjects",None)
        levels_data = validated_data.pop("levels",None)
        teaching_levels_data = validated_data.pop("teaching_levels", None) #extracts the teaching_levels from validated_data and stores it in teaching_levels_data. Removes teaching_levels from validated_data before super().update() runs.                                                                                                                                                                                                                                                                                                                                 
        
        instance = super().update(instance, validated_data)

        if levels_data is not None:
            levels = []

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

        if teaching_levels_data is not None:
                instance.teaching_levels.all().delete()

            for item in teaching_levels_data:
                level = item["level"]
                subjects = item["subjects"]

                teacher_level = TeacherLevel.objects.create(
                    teacher=instance,
                    level=level
                    )
                teacher_level.subjects.set(subjects)

        return instance