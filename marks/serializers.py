from rest_framework import serializers

from marks.models import Mark


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'

    def create(self, validated_data):
        mark, created = Mark.objects.update_or_create(
            teacher=validated_data['teacher'], solution=validated_data['solution'],
            defaults={'rate': validated_data['rate']},
        )
        return mark
