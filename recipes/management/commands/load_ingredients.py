from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv
from foodgram.settings import BASE_DIR
import os


CSV_FILE_PATH = os.path.join(BASE_DIR, 'ingredients.csv')


class Command(BaseCommand):
    help = 'Load ingredients for database'

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title, unit = row
                Ingredient.objects.get_or_create(title=title, unit=unit)
