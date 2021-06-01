from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from api.models import Course
from api.permissions import IsTeacherOrReadOnly
from api.serializers import CourseSerializer


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


class CourseUsers(APIView):
    """Add or remove user from the course"""
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