from django.urls import path
from .views import ProductListView, add_to_cart, cart_detail, checkout, order_success

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("add/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_detail, name="cart_detail"),
    path("checkout/", checkout, name="checkout"),
    path("order/<int:pk>/success/", order_success, name="order_success"),
]
from .views import warehouse_orders, advance_status

urlpatterns += [
    path("warehouse/orders/", warehouse_orders, name="warehouse_orders"),
    path("warehouse/advance/<int:pk>/", advance_status, name="advance_status"),
]
from .views import customer_order_detail
urlpatterns += [
    path("order/<int:pk>/", customer_order_detail, name="order_detail"),
]
