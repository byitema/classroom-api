from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment.save()
        return comment
