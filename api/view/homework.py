from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Lecture, Homework
from api.permissions import IsTeacherOrReadOnly
from api.serializers import HomeworkSerializer


class HomeworkList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]

    def get_my_lecture(self, request, pk):
        try:
            return Lecture.objects.get(pk=pk, teacher=request.user)
        except Lecture.DoesNotExist:
            raise Http404

    def check_lecture(self, request, course_pk, lecture_pk):
        lecture = self.get_my_lecture(request, lecture_pk)
        if lecture.course.pk != course_pk and request.user.type != 'student':
            return Response({"message": "Lecture not found."})

    def get(self, request, course_pk, lecture_pk, format=None):
        if request.user.type == 'teacher':
            homeworks = Homework.objects.filter(teacher=request.user.id,
                                                lecture_id=lecture_pk,
                                                lecture__course_id=course_pk)
        else:
            homeworks = Homework.objects.filter(lecture_id=lecture_pk,
                                                lecture__course_id=course_pk)

        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data)

    def post(self, request, course_pk, lecture_pk, format=None):
        self.check_lecture(request, course_pk, lecture_pk)

        serializer = HomeworkSerializer(data={
            'name': request.data['name'],
            'description': request.data['description'],
            'teacher': request.user.pk,
            'lecture': lecture_pk
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeworkDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    # TODO: HomeworkDetail