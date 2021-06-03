from django.urls import include, path
from . import views


urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='about_author'),
    path('tech/', views.AboutTechView.as_view(), name='about_tech'),
    ]
