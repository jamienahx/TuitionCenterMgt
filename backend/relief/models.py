from django.db import models

# Create your models here.

class ReliefTeacher(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)

    subjects = models.ManyToManyField(
        "Subject",
        related_name="relief_teachers",
        blank=True,
    )

    levels = models.ManyToManyField(
         "Level",
        related_name = "relief_teachers",
        blank = True,
        )
    

class Subject(models.Model):
    name = models.CharField(max_length=255, unique = True)

class Level(models.Model):
    name = models.CharField(max_length=255, unique = True)

class TeacherAvailability(models.Model):
    teacher = models.ForeignKey(
        ReliefTeacher,
        on_delete=models.CASCADE,
        related_name="availability",
    )

    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()