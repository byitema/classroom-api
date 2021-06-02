from rest_framework import serializers

from lectures.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

    def create(self, validated_data):
        lecture = Lecture(**validated_data)
        lecture.save()
        return lecture

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.presentation = validated_data['presentation']
        instance.description = validated_data['description']
        instance.save()
        return instance
