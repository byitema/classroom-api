from rest_framework import permissions, generics
from rest_framework.response import Response

from api.permissions import IsTeacherOrReadOnly
from lectures.mixins import CreateUpdateMixin
from lectures.models import Lecture
from lectures.serializers import LectureSerializer


class LectureList(CreateUpdateMixin, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    serializer_class = LectureSerializer

    def get_queryset(self):
        if self.request.user.type == 'teacher':
            return Lecture.objects.filter(teacher=self.request.user.id, course=self.kwargs['course_pk'])

        return Lecture.objects.filter(course=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        return self.create_update(request, self.kwargs)


class LectureDetail(CreateUpdateMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly, ]
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    def get_object(self):
        try:
            if self.request.user.type == 'teacher':
                return Lecture.objects.get(pk=self.kwargs['pk'], teacher=self.request.user)

            return Lecture.objects.get(pk=self.kwargs['pk'])
        except Lecture.DoesNotExist:
            return Response({"message": "Lecture not found"})

    def put(self, request, *args, **kwargs):
        return self.create_update(request, self.kwargs)
