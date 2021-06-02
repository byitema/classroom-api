from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)
    students = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        course = Course(
            teacher=validated_data['teacher'],
            name=validated_data['name'],
        )
        course.save()

        course.teachers.add(validated_data['teacher'])
        course.save()

        return course

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance
