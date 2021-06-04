from rest_framework import permissions, generics
from rest_framework.response import Response

from api.permissions import IsTeacherOrReadOnly
from homeworks.mixins import CreateUpdateMixin
from homeworks.models import Homework
from homeworks.serializers import HomeworkSerializer


class HomeworkList(CreateUpdateMixin, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        if self.request.user.type == 'teacher':
            return Homework.objects.filter(teacher=self.request.user.id,
                                           lecture=self.kwargs['lecture_pk'],
                                           lecture__course=self.kwargs['course_pk'])

        return Homework.objects.all(lecture=self.kwargs['lecture_pk'],
                                    lecture__course=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        return self.create_update(request, self.kwargs)


class HomeworkDetail(CreateUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def get_object(self):
        try:
            if self.request.user.type == 'teacher':
                return Homework.objects.get(pk=self.kwargs['pk'],
                                            teacher=self.request.user,
                                            lecture=self.kwargs['lecture_pk'],
                                            lecture__course=self.kwargs['course_pk'])

            return Homework.objects.get(pk=self.kwargs['pk'],
                                        lecture=self.kwargs['lecture_pk'],
                                        lecture__course=self.kwargs['course_pk'])
        except Homework.DoesNotExist:
            return Response({"message": "Homework not found"})

    def put(self, request, *args, **kwargs):
        return self.create_update(request, self.kwargs)
