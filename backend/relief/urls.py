from django.urls import path
from .views import get_teachers

#router.get("/teachers")
urlpatterns = [
    path("teachers/", get_teachers),
]