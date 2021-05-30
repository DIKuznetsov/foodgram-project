from random import choice

import factory
from factory import fuzzy

from users.factories import UserFactory

from . import models


class BaseRecipeFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    image = factory.django.ImageField(width=1000)
    description = factory.Faker('text')
    cooking_time = fuzzy.FuzzyInteger(10, 120)

    class Meta:
        model = models.Recipe


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    recipe = factory.SubFactory(BaseRecipeFactory)
    amount = fuzzy.FuzzyInteger(50, 500)

    class Meta:
        model = models.RecipeIngredient

    @factory.lazy_attribute
    def ingredient(self):
        return choice(models.Ingredient.objects.all())


class RecipeFactory(BaseRecipeFactory):

    ingredient_1 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_2 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_3 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_4 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_5 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
