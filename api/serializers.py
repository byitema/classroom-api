from rest_framework import serializers
from .models import Course, Lecture


# Course CRUD
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


# Lecture CRUD
class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

    def create(self, validated_data):
        lecture = Lecture(
            name=validated_data['name'],
            presentation=validated_data['name'],
            description=validated_data['name'],
            teacher=validated_data['name'],
            course=validated_data['name'],
        )
        lecture.save()
        return lecture
