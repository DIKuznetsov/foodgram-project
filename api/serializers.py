from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    dimension = serializers.CharField(source='unit')

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension',)
