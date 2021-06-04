from rest_framework import status
from rest_framework.response import Response

from courses.models import Course
from solutions.models import Solution
from solutions.serializers import SolutionSerializer


class CreateUpdateMixin(object):
    serializer_class = SolutionSerializer

    def create_update(self, request, kwargs):
        solution = None
        if kwargs.get('pk'):
            try:
                solution = Solution.objects.get(pk=kwargs['pk'],
                                                student=request.user,
                                                homework=kwargs['homework_pk'],
                                                homework__lecture=kwargs['lecture_pk'],
                                                homework__lecture__course=kwargs['course_pk'])
            except Solution.DoesNotExist:
                return Response({"message": "Homework not found"})

        try:
            course = Course.objects.get(pk=kwargs['course_pk'])
        except Course.DoesNotExist:
            return Response({"message": "Course not found."})

        if request.user not in course.students.all():
            return Response({"message": "Student not from this course"})

        serializer = SolutionSerializer(solution, data={
            'text': request.data['text'],
            'student': request.user.pk,
            'homework': kwargs['homework_pk']
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
