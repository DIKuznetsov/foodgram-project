from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView

from .models import Recipe, User, RecipeIngredient, Ingredient, Cart, Tag
from .forms import RecipeForm
from foodgram import settings


class IsFavoriteMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs


class BaseRecipeListView(IsFavoriteMixin, ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'recipe_list'
    paginate_by = settings.PAGE_SIZE
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title()})
        kwargs.update({'tags': Tag.objects.all()})

        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        return self.page_title

    def get_queryset(self):
        qs = super().get_queryset()
        tags = self.request.GET.getlist('tag')
        if tags:
            qs = qs.filter(tags__title__in=tags).distinct()
        return qs


class IndexView(BaseRecipeListView):
    page_title = 'Рецепты'
    template_name = 'recipes/recipe_list.html'


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    page_title = 'Избранное'
    template_name = 'recipes/recipe_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(favorites__user=self.request.user)

        return qs


class SubscriptionView(LoginRequiredMixin, ListView):
    page_title = 'Мои подписки'
    template_name = 'recipes/subscription_list.html'
    paginate_by = 6

    def get_queryset(self):
        qs = User.objects.filter(subscribers__user=self.request.user)
        return qs


class ProfileView(BaseRecipeListView):
    template_name = 'recipes/profile_recipe_list.html'

    def get(self, request, *args, **kwargs):
        self.author = get_object_or_404(User, username=kwargs.get('username'))

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        tags = self.request.GET.getlist('tag')
        qs = qs.filter(author=self.author)
        if tags:
            qs = qs.filter(tags__title__in=tags).distinct()
        return qs

    def get_context_data(self, **kwargs):
        subscription = self.author.subscribers.filter(
            user=self.request.user).exists()
        kwargs.update({'author': self.author, 'subscription': subscription})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        return self.author.get_full_name()


class RecipeDetailView(IsFavoriteMixin, DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/recipe_detail.html'

    def get(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
        self.author = recipe.author

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        subscription = self.author.subscribers.filter(
            user=self.request.user).exists()
        kwargs.update({'author': self.author, 'subscription': subscription})
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (qs.prefetch_related(
            'recipe_ingredients__ingredient').with_is_favorite(
            user_id=self.request.user.id))

        return qs


class CartView(LoginRequiredMixin, BaseRecipeListView):
    page_title = 'Мои покупки'
    template_name = 'recipes/cart.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(cart__user=self.request.user)

        return qs


@login_required
def cart_remove(request, pk):
    cart = get_object_or_404(Cart, recipe_id=pk)
    cart.delete()
    return redirect('cart')


def parse_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
                ]
    return ingredients


@login_required
def new_recipe(request):
    ERROR = 'Необходимо добавить ингридиенты'
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = parse_ingredients(request)
    if not ingredients:
        return render(request, 'recipes/new_recipe.html',
                      {'form': form, 'error': ERROR})
    if not form.is_valid():
        return render(request, 'recipes/new_recipe.html', {'form': form})
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    obj = []
    for title, amount in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        obj.append(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount,
        )
        )
    RecipeIngredient.objects.bulk_create(obj)
    form.save_m2m()
    return redirect('index')


@login_required
def recipe_edit(request, pk):
    ERROR = 'Необходимо добавить ингридиенты'
    recipe = get_object_or_404(Recipe, pk=pk)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    ingredients = parse_ingredients(request)
    if not ingredients:
        return render(
            request,
            'recipes/recipe_edit.html',
            {'form': form, 'recipe': recipe, 'error': ERROR}
        )
    if not form.is_valid():
        return render(
            request,
            'recipes/recipe_edit.html',
            {'form': form, 'recipe': recipe}
        )
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    obj = []
    for title, amount in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        obj.append(RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount,
        )
        )
    RecipeIngredient.objects.bulk_create(obj)
    form.save_m2m()
    return redirect('recipe', pk=pk)


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('index')


def purchases_download(request):
    recipes = Recipe.objects.filter(cart__user=request.user)
    ingredients_in_recipes = RecipeIngredient.objects.filter(
        recipe__in=recipes)
    d = {}
    content = ''
    for ingredient in ingredients_in_recipes:
        if ingredient.ingredient.title in d:
            d[ingredient.ingredient.title][2] += ingredient.amount
        else:
            d[ingredient.ingredient.title] = [ingredient.ingredient.title,
                                              ingredient.ingredient.unit,
                                              ingredient.amount]

    for title, unit, amount in d.values():
        content += f'{title} ({unit}) - {amount}\n'
    filename = 'purchases.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
