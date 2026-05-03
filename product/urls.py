from django.urls import path
from django.urls import path

from .views import ProductViewSet, ProductDetailsViewSet

urlpatterns = [
    path("", ProductViewSet.as_view()),  # GET, #POST
    path("<int:product_id>/", ProductDetailsViewSet.as_view()),  # GET #PUT #DELETE
]
