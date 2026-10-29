# this file it kind of like routes in Express 
from django.urls import path
from .views import get_teachers, update_teacher, delete_teacher

#router.get("/teachers")
urlpatterns = [
    path("teachers/", get_teachers),
    path("teachers/<int:teacher_id>/", update_teacher),
    path("teachers/<int:teacher_id>/delete/", delete_teacher),
]