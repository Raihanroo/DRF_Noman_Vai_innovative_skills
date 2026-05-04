from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly


class ProductViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        result = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"error": "Product does not exist!"}, status=404)
        self.check_object_permissions(request, product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"error": "Product does not exist!"}, status=404)
        self.check_object_permissions(request, product)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"error": "Product does not exist!"}, status=404)
        self.check_object_permissions(request, product)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"error": "Product does not exist!"}, status=404)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({"message": "Product deleted!"}, status=204)
