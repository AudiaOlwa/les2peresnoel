from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# Create your models here.
class Order(UUIDModel, TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tva = models.DecimalField(max_digits=10, decimal_places=2)
    redevance = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fees = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)
    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return f"Order {self.id} from {self.provider}"

    def accept(self):
        self.status = self.Status.ACCEPTED
        self.save()

    def reject(self):
        self.status = self.Status.REJECTED
        self.save()


class OrderItem(UUIDModel, TimeStampedModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "marketplace.Product",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for {self.order}"

    @property
    def get_total(self):
        return self.price * self.quantity
