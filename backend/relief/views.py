from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReliefTeacher
from .serializers import ReliefTeacherSerializer
from django.shortcuts import get_object_or_404

@api_view(["GET", "POST"])

#function displayAll (req, res)
def get_teachers(request):

    #select * from ReliefTeacher
    teachers = ReliefTeacher.objects.prefetch_related(
        "subjects",
        "levels",
        "availability"
    ) #select teachers and their related subject, levels & availability
    
    serializer = ReliefTeacherSerializer(
        teachers,
        many=True
    )

# corresponds to res.status(200).json(fetchedDatas)
    return Response(serializer.data) 

@api_view(["PATCH"])
def update_teacher(request,teacher_id):
    teacher = get_object_or_404(ReliefTeacher, id=teacher_id)

    serializer = ReliefTeacherSerializer(
        teacher,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status = 400)