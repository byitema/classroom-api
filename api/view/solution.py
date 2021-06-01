from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Course, Homework, Solution
from api.permissions import IsStudentOrReadOnly
from api.serializers import SolutionSerializer


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