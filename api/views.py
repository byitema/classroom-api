import json

from django.http import Http404
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .models import Course, Lecture, Homework, Solution
from .permissions import IsTeacherOrReadOnly, IsStudentOrReadOnly
from .serializers import CourseSerializer, LectureSerializer, HomeworkSerializer, SolutionSerializer


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


# Lecture CRUD
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
            lectures = Lecture.objects.filter(course_id=course_pk)

        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request, course_pk, format=None):
        course = self.get_my_course(request, course_pk)
        if request.user not in course.teachers.all():
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


# Homework CRUD
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


# Solution CRUD ()
class SolutionList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly, ]

    def get(self, request, course_pk, lecture_pk, homework_pk, format=None):
        if request.user.type == 'teacher':
            solutions = Solution.objects.filter(homework__teacher=request.user,
                                                homework_id=homework_pk,
                                                homework__lecture_id=lecture_pk,
                                                homework__lecture__course_id=course_pk)
        else:
            solutions = Solution.objects.filter(student=request.user,
                                                homework_id=homework_pk,
                                                homework__lecture_id=lecture_pk,
                                                homework__lecture__course_id=course_pk)

        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

    def post(self, request, course_pk, lecture_pk, homework_pk, format=None):
        if not Homework.objects.filter(pk=homework_pk,
                                       lecture_id=lecture_pk,
                                       lecture__course_id=course_pk):
            return Response({"message": "Homework not found."})

        c = Course.objects.get(pk=course_pk)

        if request.user not in c.students.all():
            return Response({"message": "Student not from this course."})

        serializer = SolutionSerializer(data={
            'text': request.data['text'],
            'student': request.user.pk,
            'homework': homework_pk
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolutionDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly, ]
    # TODO: SolutionDetail
