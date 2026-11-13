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
    def __str__(self):
        return self.name  #get the subject from the DB, get the string fron the object, then display the actual string in the field

class Level(models.Model):
    name = models.CharField(max_length=255, unique = True)
    def __str__(self):
        return self.name 

class TeacherAvailability(models.Model):
    teacher = models.ForeignKey(
        ReliefTeacher,
        on_delete=models.CASCADE,
        related_name="availability",
    )

    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

class TeacherLevel(models.Model): #inherit the Model class from the models module. TeacherLevel receives functionality from Model class
    teacher = models.ForeignKey( #fireignkey connects one DB table to another. in this case th teacher ID related to the entry ID in relief teachers
        ReliefTeacher,
        on_delete = models.CASCADE, #if you delete an entry in the teachers table, delete their record in the teachers level table too
        related_name="teaching_levels" #typically in django the default directtion of retrieval is from the table containing the foreign key into the table it is related to. Now you are going in the opposite direction, from the teachers table into the teacher_levels table.
        )

    level = models.ForeignKey(
        Level,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",

    )

    subjects = models.ManyToManyField(
        Subject,
        related_name="teacher_levels",
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields =["teacher","level"], # teacher + level combination belong in one line as a unique combination
                name = "unique_teacher_level" #name given to this constraint
            )
        ]
