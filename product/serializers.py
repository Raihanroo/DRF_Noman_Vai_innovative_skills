from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        error_messages={
            "required": "Must be a number",
            "invalid": "price must be a number",
        },
    )

    class Meta:
        model = Product
        fields = "__all__"
