from django.urls import path
from .views import (
    home,
    ProductListView, add_to_cart, cart_detail, checkout, order_success,
    warehouse_orders, advance_status, warehouse_order_detail,
    customer_order_detail,
)

urlpatterns = [

    path("", home, name="home"),
    path("catalogue/", ProductListView.as_view(), name="product_list"),
    path("add/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_detail, name="cart_detail"),
    path("checkout/", checkout, name="checkout"),
    path("order/<int:pk>/success/", order_success, name="order_success"),
    path("order/<int:pk>/", customer_order_detail, name="order_detail"),

    path("warehouse/orders/", warehouse_orders, name="warehouse_orders"),
    path("warehouse/order/<int:pk>/", warehouse_order_detail, name="warehouse_order_detail"),
    path("warehouse/advance/<int:pk>/", advance_status, name="advance_status"),
]
