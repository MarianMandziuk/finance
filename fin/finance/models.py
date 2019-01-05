from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"


class Transaction(models.Model):
    CHOICES = (
        ('spending', 'Spending'),
        ('revenue', 'Revenue'),
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type_operation = models.CharField(max_length=200, choices=CHOICES, default='spending')
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
