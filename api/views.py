from django.http import JsonResponse
from rest_framework import mixins, viewsets
from rest_framework import status

from recipes.models import Favorite, Subscription, Ingredient, Cart
from .serializers import IngredientSerializer

SUCCESS = JsonResponse({'success': True})
CREATE_FAILURE = JsonResponse({'success': False})
DELETE_FAILURE = JsonResponse({'success': False},
                              status=status.HTTP_404_NOT_FOUND)


class AddRemoveViewSet(viewsets.GenericViewSet):
    qs = None
    field_id = None

    def create(self, request, format=None):
        try:
            self.qs.create(user=request.user,
                           **{self.field_id: request.data['id']})
            return SUCCESS
        except 'Can not do that':
            return CREATE_FAILURE

    def destroy(self, request, pk, format=None):
        deleted, _ = self.qs.filter(user=request.user,
                                    **{self.field_id: pk}).delete()
        if deleted:
            return SUCCESS
        return DELETE_FAILURE


class AddRemoveFavoritesViewSet(AddRemoveViewSet):
    qs = Favorite.objects.all()
    field_id = 'recipe_id'


class AddRemoveSubscriptionsViewSet(AddRemoveViewSet):
    qs = Subscription.objects.all()
    field_id = 'author_id'


class AddRemovePurchasesViewSet(AddRemoveViewSet):
    qs = Cart.objects.all()
    field_id = 'recipe_id'


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredient = self.request.query_params.get('query')
        if ingredient is not None:
            queryset = queryset.filter(title__startswith=ingredient)
        return queryset
