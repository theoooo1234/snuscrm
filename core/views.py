from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Variant, Company, Order, OrderLine
from .forms import AddToCartForm
from .cart import Cart




class ProductListView(ListView):
    model = Variant
    template_name = "core/product_list.html"
    context_object_name = "variants"


def add_to_cart(request):
    form = AddToCartForm(request.POST)
    if form.is_valid():
        Cart(request).add(form.cleaned_data["variant_id"], form.cleaned_data["quantity"])
    return redirect("product_list")


def cart_detail(request):
    cart = Cart(request)
    total = sum(line_total for _, _, line_total in cart.items())
    return render(request, "core/cart_detail.html", {"cart": cart, "total": total})




@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect("product_list")

    company = Company.objects.first()                     # placeholder
    order = Order.objects.create(company=company, created_by=request.user)

    for variant, qty, _ in cart.items():
        OrderLine.objects.create(order=order, variant=variant, quantity=qty)
        variant.stock_units -= qty
        variant.save()

    cart.clear()
    return redirect(reverse("order_success", args=[order.id]))


@login_required
def order_success(request, pk):
    return render(request, "core/order_success.html", {"order_id": pk})




def in_warehouse(user):
    return user.is_authenticated and user.groups.filter(name="Warehouse").exists()


@user_passes_test(in_warehouse)
def warehouse_orders(request):
    orders = Order.objects.all().order_by("-id")
    return render(request, "core/warehouse_orders.html", {"orders": orders})


@user_passes_test(in_warehouse)
def advance_status(request, pk):
    order = Order.objects.get(pk=pk)
    flow = ["CREATED", "PACKING", "SHIPPED", "DELIVERED"]

    try:
        next_status = flow[flow.index(order.status) + 1]
        order.status = next_status
        order.save()
    except (ValueError, IndexError):
        pass  # already at final state

    return redirect("warehouse_orders")




def customer_order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, "core/order_detail.html", {"order": order})
