from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company",
    )
    name             = models.CharField(max_length=120, unique=True)
    country          = models.CharField(max_length=60, blank=True)
    vat_number       = models.CharField(max_length=40, blank=True)
    register_number  = models.CharField(max_length=40, blank=True)
    email            = models.EmailField(blank=True)
    phone            = models.CharField(max_length=40, blank=True)
    delivery_address = models.TextField(blank=True)
    contact_person   = models.CharField(max_length=120, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Product(models.Model):
    name        = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    product        = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    strength_mg_g  = models.PositiveSmallIntegerField()
    sku            = models.CharField(max_length=40, unique=True)
    price          = models.DecimalField(max_digits=8, decimal_places=2)
    stock_units    = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "strength_mg_g")

    def __str__(self):
        return f"{self.product.name} – {self.strength_mg_g} mg/g"


class Order(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "Created"),
        ("PACKING", "Packing / Manufacturing"),
        ("SHIPPED", "In Transit"),
        ("DELIVERED", "Delivered"),
    ]

    company     = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_by  = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at  = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CREATED")

    def __str__(self):
        return f"Order #{self.id} – {self.company.name}"


class OrderLine(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    variant  = models.ForeignKey(Variant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    @property
    def line_total(self):
        return self.quantity * self.variant.price
