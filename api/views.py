from django.http import JsonResponse
from rest_framework import mixins, viewsets

from recipes.models import Favorite, Subscription, Ingredient, Cart
from .serializers import IngredientSerializer

SUCCESS = JsonResponse({'success': True})
FAILURE = JsonResponse({'success': False})


class AddRemoveFavoritesViewSet(viewsets.GenericViewSet):

    def create(self, request, format=None):
        obj, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        if obj:
            return FAILURE
        return SUCCESS

    def destroy(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        if Favorite.objects.filter(recipe_id=pk, user=request.user).exists():
            return FAILURE
        return SUCCESS


class AddRemoveSubscriptionsViewSet(viewsets.GenericViewSet):

    def create(self, request, format=None):
        obj, created = Subscription.objects.get_or_create(
            user=request.user,
            author_id=request.data['id'],
        )
        if obj:
            return FAILURE
        return SUCCESS

    def destroy(self, request, pk, format=None):
        Subscription.objects.filter(author_id=pk,
                                    user=request.user).delete()
        if Subscription.objects.filter(author_id=pk,
                                       user=request.user).exists():
            return FAILURE
        return SUCCESS


class AddRemovePurchasesViewSet(viewsets.GenericViewSet):

    def create(self, request, format=None):
        obj, created = Cart.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        if obj:
            return FAILURE
        return SUCCESS

    def destroy(self, request, pk, format=None):
        Cart.objects.filter(recipe_id=pk,
                            user=request.user).delete()
        if Cart.objects.filter(recipe_id=pk,
                            user=request.user).exists():
            return FAILURE
        return SUCCESS


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredient = self.request.query_params.get('query')
        if ingredient is not None:
            queryset = queryset.filter(title__startswith=ingredient)
        return queryset
