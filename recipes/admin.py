from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'unit',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'unit',
        'title',
    )


@register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
    )


@register(models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = (
        'ingredient',
        'recipe',
        'amount',
    )
    search_fields = (
        'ingredient',
        'recipe',
    )


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    min_num = 1
    extra = 0


@register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'pub_date',
    )
    search_fields = (
        'name',
        'tags',
    )
    list_filter = (
        'author',
        'name',
    )
    autocomplete_fields = (
        'ingredients',
    )
    inlines = (
        RecipeIngredientInline,
    )


@register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )


@register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'author',
    )
    search_fields = (
        'user',
        'author',
    )


@register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    fields = (
        'user',
    )
    search_fields = (
        'user',
    )
