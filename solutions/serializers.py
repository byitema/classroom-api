from rest_framework import serializers

from solutions.models import Solution


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
