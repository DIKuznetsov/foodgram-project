from django import forms
from django.forms import CheckboxSelectMultiple, FileInput
from django.shortcuts import get_object_or_404

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name',
            'image',
            'tags',
            'description',
            'cooking_time',
        ]
        widgets = {
            'tags': CheckboxSelectMultiple(),
            'image': FileInput(),
        }

    def clean_ingridient(self):
        super().clean()
        new_ingridients_list = {}
        for key, title in self.data.items():
            if 'nameIngredient_' in key:
                elem = key.split("_")
                new_ingridients_list[title] = int(self.data[f'valueIngredient'
                                                            f'_{elem[1]}'])

        ing_titles = self.data.getlist("nameIngredient")
        ing_amount = self.data.getlist("valueIngredient")

        for title, amount in new_ingridients_list.items():
            ing_titles.append(title)
            ing_amount.append(amount)

        clean_items = {}
        for number, item in enumerate(ing_titles):
            ingridient = get_object_or_404(Ingredient, title=item)
            clean_items[ingridient] = ing_amount[number]
        self.cleaned_data['items'] = clean_items
        return self.cleaned_data['items']
