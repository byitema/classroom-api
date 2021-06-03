from rest_framework import serializers

from courses.models import Course
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(read_only=False, many=True, queryset=User.objects.all())
    students = serializers.PrimaryKeyRelatedField(read_only=False, many=True, queryset=User.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        course = Course(
            name=validated_data.get('name'),
            teacher=validated_data.get('teacher'),
        )
        course.save()

        course.teachers.set(validated_data.get('teachers', []))
        course.teachers.add(validated_data['teacher'])
        course.students.set(validated_data.get('students', []))
        course.save()

        return course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.teachers.set(validated_data.get('teachers', instance.teachers.all()))
        instance.students.set(validated_data.get('students', instance.students.all()))
        instance.save()
        return instance
