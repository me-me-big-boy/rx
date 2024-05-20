import calendar
import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models import BaseModel
from rx.choices import MeasurementUnit


class Delivery(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "deliveries"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)


class Agent(BaseModel):
    names = ArrayField(models.CharField(max_length=255))

    # Relationships
    categories = models.ManyToManyField(
        to="rx.Category",
        related_name="agents",
    )

    class Meta:
        ordering = ("names",)

    @property
    def category_names(self) -> str:
        return ", ".join(cat.name for cat in self.categories.all())

    def __str__(self) -> str:
        text, *rest = self.names
        if rest:
            aliases = ", ".join(rest)
            text = f"{text} (aka {aliases})"
        return text


class Medicine(BaseModel):
    name = models.CharField(max_length=255)

    # Quantity
    mu = models.CharField(
        verbose_name="measurement unit",
        choices=MeasurementUnit,
        default=MeasurementUnit.UNKNOWN,
    )
    # quantity and total quantity are stored in ``Unit`` model

    # Relationships
    delivery = models.ForeignKey(
        to="rx.Delivery",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    agents = models.ManyToManyField(
        to="rx.Agent",
        through="rx.Ingredient",
    )

    class Meta:
        ordering = ("name",)

    @property
    def composition(self) -> str:
        return ", ".join(
            f"{i.agent} = {i.quantity}{i.get_mu_display()}"
            for i in self.ingredient_set.all()
        )

    @property
    def quantities(self) -> tuple[str, str]:
        quant = self.unit_set.filter(is_discarded=False).aggregate(
            quantity=models.Sum("quantity"),
            init_quantity=models.Sum("init_quantity"),
        )
        not_expired_quant = self.unit_set.filter(
            is_discarded=False, expires_on__gte=datetime.date.today()
        ).aggregate(quantity=models.Sum("quantity"))
        return {
            "init_quantity": quant["init_quantity"],
            "quantity": quant["quantity"],
            "valid_quantity": not_expired_quant["quantity"],
        }


class Ingredient(BaseModel):
    # Mandatory relationships
    medicine = models.ForeignKey(to="Medicine", on_delete=models.CASCADE)
    agent = models.ForeignKey(to="Agent", on_delete=models.CASCADE)

    # Quantity
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    mu = models.CharField(
        verbose_name="measurement unit",
        choices=MeasurementUnit,
        default=MeasurementUnit.UNKNOWN,
    )

    def __str__(self) -> str:
        return f"{self.medicine} × {self.agent}"


class Unit(BaseModel):
    # Quantity
    quantity = models.DecimalField(
        verbose_name="available quantity",
        max_digits=8,
        decimal_places=2,
    )
    init_quantity = models.DecimalField(
        verbose_name="initial quantity",
        max_digits=8,
        decimal_places=2,
    )
    # measurement unit is stored in ``Medicine`` model

    # Cost
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )
    currency = models.CharField(max_length=3, blank=True, null=True)

    # Expiration
    expires_on = models.DateField()
    is_discarded = models.BooleanField(default=False)

    # Relationships
    medicine = models.ForeignKey(to="Medicine", on_delete=models.CASCADE)

    class Meta:
        ordering = ("medicine__name",)

    @property
    def is_expired(self) -> bool:
        return self.expires_on < datetime.date.today()

    def __str__(self) -> str:
        return f"{self.medicine} ({self.quantity}/{self.medicine.get_mu_display()})"

    def save(self, *args, **kwargs):
        # Always push expiration date to the last date of the specified month.
        if isinstance(self.expires_on, datetime.date):
            _, last = calendar.monthrange(self.expires_on.year, self.expires_on.month)
            self.expires_on = datetime.date(
                self.expires_on.year,
                self.expires_on.month,
                last,
            )

        super().save(*args, **kwargs)
