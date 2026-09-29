from django.db import models

# Create your models here.

class ReliefTeacher(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)

class Subject(models.Model):
    name = models.CharField(max_length=255, unique = True)

class Level(models.Model):
    name = models.CharField(max_length=255, unique = True)