from django.http import Http404
from rest_framework import permissions, generics

from api.permissions import IsTeacherOrReadOnly
from courses.models import Course
from courses.serializers import CourseSerializer


class CourseList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.type == 'teacher':
            return Course.objects.filter(teacher=self.request.user.id)

        return Course.objects.all()


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_object(self):
        try:
            if self.request.user.type == 'teacher':
                return Course.objects.get(pk=self.kwargs[self.lookup_field], teacher=self.request.user)

            return Course.objects.get(pk=self.kwargs[self.lookup_field])
        except Course.DoesNotExist:
            raise Http404
