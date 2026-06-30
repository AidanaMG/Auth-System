from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from permissions.checker import get_user_permission

class FakeObject:
    def __init__(self, owner_id):
        self.owner_id = owner_id


MOCK_PRODUCTS = [
    {"id": 1, "name": "Product 1", "owner_id": 16},
    {"id": 2, "name": "Product 2", "owner_id": 16},
    {"id": 3, "name": "Product 3", "owner_id": 16},
    {"id": 4, "name": "Product 4", "owner_id": 16},
    {"id": 5, "name": "Product 5", "owner_id": 16},
    {"id": 6, "name": "Product 6", "owner_id": 16},
    {"id": 7, "name": "Product 7", "owner_id": 16},
]


@method_decorator(csrf_exempt, name="dispatch")
class ProductListView(APIView):
    def get(self, request):
        permission = get_user_permission(request._request.jwt_user, "products", "read")

        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)

        if permission == "all":
            return Response(MOCK_PRODUCTS)

        own = [p for p in MOCK_PRODUCTS if p["owner_id"] == request._request.jwt_user.id]
        return Response(own)

    def post(self, request):
        permission = get_user_permission(request._request.jwt_user, "products", "create")
        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)

        new_product = {"id": len(MOCK_PRODUCTS) + 1, "name": request.data.get("name"), "owner_id": request._request.jwt_user.id}
        MOCK_PRODUCTS.append(new_product)
        return Response(new_product, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        user = request._request.jwt_user
        product = next((p for p in MOCK_PRODUCTS if p["id"] == pk), None)
        if product is None:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        fake_obj = FakeObject(owner_id=product["owner_id"])
        permission = get_user_permission(user, "products", "update")

        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)
        if permission == "own" and fake_obj.owner_id != user.id:
            return Response({"detail": "You can edit only your own products"}, status=status.HTTP_403_FORBIDDEN)

        product["name"] = request.data.get("name", product["name"])
        return Response(product)
    

MOCK_ORDERS = [
    {"id": 1, "product": "Product 1", "owner_id": 15},
    {"id": 2, "product": "Product 2", "owner_id": 15},
    {"id": 3, "product": "Product 3", "owner_id": 16},
    {"id": 4, "product": "Product 4", "owner_id": 13},
]

MOCK_REVIEWS = [
    {"id": 1, "text": "Good product!", "owner_id": 15},
    {"id": 2, "text": "I recommend it to everyone.", "owner_id": 16},
    {"id": 3, "text": "Didn't like :(", "owner_id": 15},
]


@method_decorator(csrf_exempt, name="dispatch")
class OrderListView(APIView):
    def get(self, request):
        user = request._request.jwt_user
        permission = get_user_permission(user, "orders", "read")

        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)
        if permission == "all":
            return Response(MOCK_ORDERS)

        own = [o for o in MOCK_ORDERS if o["owner_id"] == user.id]
        return Response(own)

    def post(self, request):
        user = request._request.jwt_user
        permission = get_user_permission(user, "orders", "create")
        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)

        new_order = {"id": len(MOCK_ORDERS) + 1, "product": request.data.get("product"), "owner_id": user.id}
        MOCK_ORDERS.append(new_order)
        return Response(new_order, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        user = request._request.jwt_user
        order = next((o for o in MOCK_ORDERS if o["id"] == pk), None)
        if order is None:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        fake_obj = FakeObject(owner_id=order["owner_id"])
        permission = get_user_permission(user, "orders", "update")

        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)
        if permission == "own" and fake_obj.owner_id != user.id:
            return Response({"detail": "You can edit only your own orders"}, status=status.HTTP_403_FORBIDDEN)

        order["product"] = request.data.get("product", order["product"])
        return Response(order)


@method_decorator(csrf_exempt, name="dispatch")
class ReviewListView(APIView):
    def get(self, request):
        user = request._request.jwt_user
        permission = get_user_permission(user, "reviews", "read")

        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)
        if permission == "all":
            return Response(MOCK_REVIEWS)

        own = [r for r in MOCK_REVIEWS if r["owner_id"] == user.id]
        return Response(own)

    def post(self, request):
        user = request._request.jwt_user
        permission = get_user_permission(user, "reviews", "create")
        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)

        new_review = {"id": len(MOCK_REVIEWS) + 1, "text": request.data.get("text"), "owner_id": user.id}
        MOCK_REVIEWS.append(new_review)
        return Response(new_review, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        user = request._request.jwt_user
        review = next((r for r in MOCK_REVIEWS if r["id"] == pk), None)
        if review is None:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        fake_obj = FakeObject(owner_id=review["owner_id"])
        permission = get_user_permission(user, "reviews", "update")

        if permission == "none":
            return Response({"detail": "Access is denied"}, status=status.HTTP_403_FORBIDDEN)
        if permission == "own" and fake_obj.owner_id != user.id:
            return Response({"detail": "You can edit only your own reviews"}, status=status.HTTP_403_FORBIDDEN)

        review["text"] = request.data.get("text", review["text"])
        return Response(review)
