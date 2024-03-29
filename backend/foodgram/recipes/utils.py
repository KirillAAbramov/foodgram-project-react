import io

from django.db.models import F, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient
from .serializers import FavoriteSerializer


def get_shopping_list(self, request):
    user = request.user
    shopping_list = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user).values(
        name=F('ingredients__name'),
        unit=F('ingredients__measurement_unit')
    ).annotate(amount=Sum('amount'))
    font = 'DejaVuSerif'
    pdfmetrics.registerFont(
        TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer)
    pdf_file.setFont(font, 24)
    pdf_file.drawString(
        150,
        800,
        'Список покупок.'
    )
    pdf_file.setFont(font, 14)
    from_bottom = 750
    for number, ingredient in enumerate(shopping_list, start=1):
        pdf_file.drawString(
            50,
            from_bottom,
            f'{number}.  {ingredient["name"]} - {ingredient["amount"]} '
            f'{ingredient["unit"]}'
        )
        from_bottom -= 20
        if from_bottom <= 50:
            from_bottom = 800
            pdf_file.showPage()
            pdf_file.setFont(font, 14)
    pdf_file.showPage()
    pdf_file.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='shopping_list.pdf')


def delete(request, id, model):
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    obj = get_object_or_404(model, user=user, recipe=recipe)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def post(request, id, model):
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    model.objects.get_or_create(user=user, recipe=recipe)
    serializer = FavoriteSerializer(recipe, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)
