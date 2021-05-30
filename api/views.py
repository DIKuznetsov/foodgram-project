from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, viewsets

from recipes.models import Favorite, Subscription, Ingredient, Cart
from .serializers import IngredientSerializer


class AddToFavorites(APIView):

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):

    def delete(self, request, pk, format=None):
        Favorite.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddSubscriptions(APIView):

    def post(self, request, format=None):
        Subscription.objects.get_or_create(
            user=request.user,
            author_id=request.data['id'],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveSubscriptions(APIView):

    def delete(self, request, pk, format=None):
        Subscription.objects.filter(author_id=pk,
                                    user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddPurchases(APIView):

    def post(self, request, format=None):
        Cart.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemovePurchases(APIView):

    def delete(self, request, pk, format=None):
        Cart.objects.filter(recipe_id=pk,
                            user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredient = self.request.query_params.get('query')
        if ingredient is not None:
            queryset = queryset.filter(title__startswith=ingredient)
        return queryset
