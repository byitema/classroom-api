import json

from rest_framework import status
from rest_framework.response import Response

from courses.models import Course
from lectures.models import Lecture
from lectures.serializers import LectureSerializer


class CreateUpdateMixin(object):
    serializer_class = LectureSerializer

    def create_update(self, request, kwargs):
        lecture = None
        if kwargs.get('pk'):
            try:
                lecture = Lecture.objects.get(pk=kwargs.get('pk'), teacher=request.user)
            except Lecture.DoesNotExist:
                return Response({"message": "Lecture not found"})

        course = Course.objects.get(pk=kwargs['course_pk'], teacher=request.user)
        if request.user not in course.teachers.all():
            return Response({"message": "Course not found."})

        serializer = LectureSerializer(lecture, data={
            'name': json.loads(request.data['data'])['name'],
            'presentation': request.data['file'],
            'description': json.loads(request.data['data'])['description'],
            'teacher': request.user.pk,
            'course': kwargs['course_pk']
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
