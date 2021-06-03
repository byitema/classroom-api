import json

from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsTeacherOrReadOnly
from courses.models import Course
from lectures.models import Lecture
from lectures.serializers import LectureSerializer


class LectureList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    serializer_class = LectureSerializer

    def get_queryset(self):
        if self.request.user.type == 'teacher':
            return Lecture.objects.filter(teacher=self.request.user.id, course=self.kwargs['course_pk'])

        return Lecture.objects.all(course=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['course_pk'], teacher=request.user)
        if request.user not in course.teachers.all():
            return Response({"message": "Course not found."})

        serializer = LectureSerializer(data={
            'name': json.loads(request.data['data'])['name'],
            'presentation': request.data['file'],
            'description': json.loads(request.data['data'])['description'],
            'teacher': request.user.pk,
            'course': self.kwargs['course_pk']
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def get_my_course(self, request, pk):
        try:
            return Course.objects.get(pk=pk, teacher=request.user)
        except Course.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def get_my_object(self, request, pk):
        try:
            return Lecture.objects.get(pk=pk, teacher=request.user)
        except Lecture.DoesNotExist:
            raise Http404

    def get(self, request, course_pk, pk, format=None):
        if request.user.type == 'teacher':
            lecture = self.get_my_object(request, pk)
        else:
            lecture = self.get_object(pk)
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)

    def put(self, request, course_pk, pk, format=None):
        lecture = self.get_my_object(request, pk)
        if not lecture:
            return Response({"message": "Lecture not found."})

        course = self.get_my_course(request, course_pk)
        if request.user not in course.teachers:
            return Response({"message": "Course not found."})

        serializer = LectureSerializer(lecture, data={
            'name': json.loads(request.data['data'])['name'],
            'presentation': request.data['file'],
            'description': json.loads(request.data['data'])['description'],
            'teacher': lecture.teacher.pk,
            'course': lecture.course.pk
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_pk, pk, format=None):
        lecture = self.get_my_object(request, pk)
        lecture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
