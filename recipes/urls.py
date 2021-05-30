from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from api.views import (AddSubscriptions, AddToFavorites, RemoveFromFavorites,
                       RemoveSubscriptions, IngredientViewSet, AddPurchases,
                       RemovePurchases)

router = DefaultRouter(trailing_slash=False)
router.register(r'ingredients', IngredientViewSet, basename='ingredients')


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
    path('v1/favorites/', AddToFavorites.as_view()),
    path('v1/favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('v1/subscriptions/', AddSubscriptions.as_view()),
    path('v1/subscriptions/<int:pk>/', RemoveSubscriptions.as_view()),
    path('v1/purchases/', AddPurchases.as_view()),
    path('v1/purchases/<int:pk>/', RemovePurchases.as_view()),
    path('v1/', include(router.urls)),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(api_patterns)),
]
