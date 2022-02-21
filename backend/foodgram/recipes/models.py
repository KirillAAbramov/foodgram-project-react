from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        unique=True,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to="media/recipes/images/"
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1,
                                      message='Минимальное время'
                                              'приготовления - одна минута')],
        verbose_name='Время приготовления (в минутах)'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def favorites_count(self):
        return self.favorites.count()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_to_recipe'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='ingredient_to_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        validators=(
            MinValueValidator(1, 'Минимальное количество ингредиентов 1'),
        )
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='unique_recipe_ingredients'
            )
        ]
        verbose_name = 'Рецепт и ингредиенты'
        verbose_name_plural = 'Рецепты и ингредиенты'

    def __str__(self):
        return f'{self.recipe.name} {self.ingredients.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='favorite')
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user}, {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='shopping_cart')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user}, {self.recipe}'
