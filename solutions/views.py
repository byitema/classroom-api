from rest_framework import permissions, generics
from rest_framework.response import Response

from api.permissions import IsStudentOrReadOnly
from solutions.mixins import CreateUpdateMixin
from solutions.models import Solution
from solutions.serializers import SolutionSerializer


class SolutionList(CreateUpdateMixin, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly, ]
    serializer_class = SolutionSerializer

    def get_queryset(self):
        if self.request.user.type == 'teacher':
            return Solution.objects.filter(homework=self.kwargs['homework_pk'],
                                           homework__lecture=self.kwargs['lecture_pk'],
                                           homework__lecture__course=self.kwargs['course_pk'])

        return Solution.objects.filter(student=self.request.user,
                                       homework=self.kwargs['homework_pk'],
                                       homework__lecture=self.kwargs['lecture_pk'],
                                       homework__lecture__course=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        return self.create_update(request, self.kwargs)


class SolutionDetail(CreateUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudentOrReadOnly, ]
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()

    def get_object(self):
        try:
            if self.request.user.type == 'teacher':
                return Solution.objects.get(pk=self.kwargs['pk'],
                                            homework=self.kwargs['homework_pk'],
                                            homework__lecture=self.kwargs['lecture_pk'],
                                            homework__lecture__course=self.kwargs['course_pk'])

            return Solution.objects.get(pk=self.kwargs['pk'],
                                        student=self.request.user,
                                        homework=self.kwargs['homework_pk'],
                                        homework__lecture=self.kwargs['lecture_pk'],
                                        homework__lecture__course=self.kwargs['course_pk'])
        except Solution.DoesNotExist:
            return Response({"message": "Solution not found"})

    def put(self, request, *args, **kwargs):
        return self.create_update(request, self.kwargs)
