from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from api.views import (IngredientViewSet, AddRemoveFavoritesViewSet,
                       AddRemoveSubscriptionsViewSet,
                       AddRemovePurchasesViewSet)

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'favorites', AddRemoveFavoritesViewSet,
                basename='favorites')
router.register(r'subscriptions', AddRemoveSubscriptionsViewSet,
                basename='subscriptions')
router.register(r'purchases', AddRemovePurchasesViewSet,
                basename='purchases')


views_patterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('favorites/', views.FavoriteView.as_view(), name='favorites'),
    path('subscriptions/', views.SubscriptionView.as_view(),
         name='subscriptions'),
    path('profiles/<str:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe'),
    path('new/', views.new_recipe, name='new'),
    path('recipes/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:pk>/delete/',
         views.recipe_delete,
         name='recipe_delete'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete', views.cart_remove, name='cart_remove'),
    path('purchases-download', views.purchases_download,
         name='purchases_download')
]

api_patterns = [
    path('v1/', include(router.urls)),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(api_patterns)),
]
