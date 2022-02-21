import json

from django.core.management.base import BaseCommand
from django.db import transaction

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        json_file_path = (
            '/Users/kirillabramov/Dev/'
            'foodgram-project-react/data/ingredients.json')

        with open(json_file_path, encoding='utf-8') as f:
            data = json.load(f)
            with transaction.atomic():
                for item in data:
                    ingredient = Ingredient.objects.get_or_create(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )[0]
                    ingredient.save()
