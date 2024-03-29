from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .filters import IngredientSearchFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import LimitPageNumberPagination
from .permissions import AuthorOrReadOnly
from .serializers import (
    CreateRecipeSerializer, IngredientSerializer, TagSerializer,
    ViewRecipeSerializer,
)
from .utils import delete, get_shopping_list, post


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ['get']


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ['get']
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ViewRecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = LimitPageNumberPagination
    filterset_class = RecipeFilter
    filterset_fields = ('tags', 'author')
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewRecipeSerializer
        return CreateRecipeSerializer


class APIFavorite(APIView):

    def delete(self, request, id):
        return delete(request, id, Favorite)

    def post(self, request, id):
        return post(request, id, Favorite)


class APIShoppingCart(APIView):

    def get(self, request):
        return get_shopping_list(self, request)

    def delete(self, request, id):
        return delete(request, id, ShoppingCart)

    def post(self, request, id):
        return post(request, id, ShoppingCart)
