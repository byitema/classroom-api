from rest_framework import status
from rest_framework.response import Response

from homeworks.models import Homework
from homeworks.serializers import HomeworkSerializer
from lectures.models import Lecture


class CreateUpdateMixin(object):
    serializer_class = HomeworkSerializer

    def create_update(self, request, kwargs):
        homework = None
        if kwargs.get('pk'):
            try:
                homework = Homework.objects.get(pk=kwargs['pk'],
                                                teacher=request.user,
                                                lecture=kwargs['lecture_pk'],
                                                lecture__course=kwargs['course_pk'])
            except Homework.DoesNotExist:
                return Response({"message": "Homework not found"})

        try:
            lecture = Lecture.objects.get(pk=kwargs['lecture_pk'],
                                          teacher=request.user,
                                          course=kwargs['course_pk'])
        except Lecture.DoesNotExist:
            return Response({"message": "Lecture not found."})

        serializer = HomeworkSerializer(homework, data={
            'name': request.data['name'],
            'description': request.data['description'],
            'teacher': request.user.pk,
            'lecture': lecture.pk
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
