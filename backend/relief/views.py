from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReliefTeacher
from .serializers import ReliefTeacherSerializer

@api_view(["GET"])

#function displayAll (req, res)
def get_teachers(request):

    #select * from ReliefTeacher
    teachers = ReliefTeacher.objects.all()
    
    serializer = ReliefTeacherSerializer(
        teachers,
        many=True
    )

# corresponds to res.status(200).json(fetchedDatas)
    return Response(serializer.data) 