from rest_framework import serializers

from homeworks.models import Homework


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

    def create(self, validated_data):
        homework = Homework(**validated_data)
        homework.save()
        return homework

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.description = validated_data['description']
        instance.save()
        return instance
