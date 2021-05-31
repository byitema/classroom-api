import json

from django.http import Http404
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .models import Course, Lecture
from .permissions import IsTeacherOrReadOnly
from .serializers import CourseSerializer, LectureSerializer


# Course CRUD
class CourseList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def get(self, request):
        if request.user.type == 'teacher':
            courses = Course.objects.filter(teacher=request.user.id)
        else:
            courses = Course.objects.all()

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get_my_object(self, request, pk):
        try:
            return Course.objects.get(pk=pk, teacher=request.user)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if request.user.type == 'teacher':
            course = self.get_my_object(request, pk)
        else:
            course = self.get_object(pk)

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        course = self.get_my_object(request, pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        course = self.get_my_object(request, pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# add student to the course
class CourseUsers(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def get_my_course(self, request, pk):
        try:
            return Course.objects.get(pk=pk, teacher=request.user)
        except Course.DoesNotExist:
            raise Http404

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, course_pk, user_pk, format=None):
        course = self.get_my_course(course_pk)
        if not course:
            return Response({"message": "Course not found."})
        user = self.get_user(user_pk)
        if not user:
            return Response({"message": "User not found."})

        if user.type == 'teacher':
            course.teachers.add(user)
        elif user.type == 'student':
            course.students.add(user)

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def delete(self, request, course_pk, user_pk, format=None):
        course = self.get_my_course(course_pk)
        if not course:
            return Response({"message": "Course not found."})
        user = self.get_user(user_pk)
        if not user:
            return Response({"message": "User not found."})

        if user.type == 'teacher':
            course.teachers.remove(user)
        elif user.type == 'student':
            course.students.remove(user)

        serializer = CourseSerializer(course)
        return Response(serializer.data)


class LectureList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    parser_classes = [MultiPartParser, ]

    def get_my_course(self, request, pk):
        try:
            return Course.objects.get(pk=pk, teacher=request.user)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, course_pk, format=None):
        if request.user.type == 'teacher':
            lectures = Lecture.objects.filter(teacher=request.user.id, course=course_pk)
        else:
            lectures = Lecture.objects.filter(course=course_pk)

        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request, course_pk, format=None):
        course = self.get_my_course(request, course_pk)
        if request.user not in course.teachers:
            return Response({"message": "Course not found."})

        serializer = LectureSerializer(data={
            'name': json.loads(request.data['data'])['name'],
            'presentation': request.data['file'],
            'description': json.loads(request.data['data'])['description'],
            'teacher': request.user.pk,
            'course': course_pk
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LectureDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

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
