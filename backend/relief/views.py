from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReliefTeacher
from .serializers import ReliefTeacherSerializer

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