from rest_framework import permissions, generics, status
from rest_framework.response import Response

from api.permissions import IsTeacherOrReadOnly
from marks.models import Mark
from marks.serializers import MarkSerializer
from solutions.models import Solution


class MarkView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    serializer_class = MarkSerializer

    def get_queryset(self):
        if self.request.user.type == 'teacher':
            return Mark.objects.filter(teacher=self.request.user,
                                       solution=self.kwargs['solution_pk'],
                                       solution__homework=self.kwargs['homework_pk'],
                                       solution__homework__lecture=self.kwargs['lecture_pk'],
                                       solution__homework__lecture__course=self.kwargs['course_pk'])

        return Mark.objects.filter(solution=self.kwargs['solution_pk'],
                                   solution__homework=self.kwargs['homework_pk'],
                                   solution__homework__lecture=self.kwargs['lecture_pk'],
                                   solution__homework__lecture__course=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        """Create/Update mark"""

        try:
            solution = Solution.objects.get(pk=kwargs['solution_pk'],
                                            homework=self.kwargs['homework_pk'],
                                            homework__lecture=self.kwargs['lecture_pk'],
                                            homework__lecture__course=self.kwargs['course_pk'])
        except Solution.DoesNotExist:
            return Response({"message": "Solution not found."})

        if request.user != solution.homework.teacher:
            return Response({"message": "Teacher can't rate this homework"})

        serializer = MarkSerializer(data={
            'rate': request.data['rate'],
            'teacher': request.user.pk,
            'solution': kwargs['solution_pk']
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
