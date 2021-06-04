from rest_framework import permissions, generics, status
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer
from marks.models import Mark


class CommentView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(mark__solution=self.kwargs['solution_pk'],
                                      mark__solution__homework=self.kwargs['homework_pk'],
                                      mark__solution__homework__lecture=self.kwargs['lecture_pk'],
                                      mark__solution__homework__lecture__course=self.kwargs['course_pk'])

    def post(self, request, *args, **kwargs):
        try:
            mark = Mark.objects.get(pk=self.kwargs['mark_pk'],
                                    solution=self.kwargs['solution_pk'],
                                    solution__homework=self.kwargs['homework_pk'],
                                    solution__homework__lecture=self.kwargs['lecture_pk'],
                                    solution__homework__lecture__course=self.kwargs['course_pk'])
        except Mark.DoesNotExist:
            return Response({"message": "Mark not found"})

        if request.user.type == 'teacher':
            if request.user != mark.teacher:
                return Response({"message": "Teacher can't comment this mark"})
        else:
            if request.user != mark.solution.student:
                return Response({"message": "Student can't comment this mark"})

        serializer = CommentSerializer(data={
            'text': request.data['text'],
            'user': request.user.pk,
            'mark': mark.pk
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
