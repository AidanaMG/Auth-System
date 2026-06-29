from django.urls import path
from .views import ProductListView
from .views import OrderListView
from .views import ReviewListView

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/<int:pk>/", ProductListView.as_view()),
    path("orders/", OrderListView.as_view()),
    path("orders/<int:pk>/", OrderListView.as_view()),
    path("reviews/", ReviewListView.as_view()),
    path("reviews/<int:pk>/", ReviewListView.as_view()),
]