from rest_framework import serializers
from .models import Course, Lecture, Homework, Solution


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

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance


# Lecture CRUD
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


# Homework CRUD
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


# Solution CRUD
class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'

    def create(self, validated_data):
        solution = Solution(**validated_data)
        solution.save()
        return solution

    def update(self, instance, validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance
