from django.db import models
from django.utils import timezone

# Create your models here.


class TypeCategoryModel(models.Model):
    name = models.CharField(
        max_length=20, verbose_name="Name", blank=False, unique=True)

    class Meta:
        db_table = "type_category"
        verbose_name = "Type Category"
        verbose_name_plural = "Type Categories"

    def __str__(self) -> str:
        return self.name


class CategoryModel(models.Model):
    title = models.CharField(
        max_length=30, verbose_name="Title", blank=False, unique=True)
    fk_id_type = models.ForeignKey(TypeCategoryModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class RecordModel(models.Model):
    mount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, verbose_name="Mount")
    note = models.TextField(null=True, blank=True)
    register_date = models.DateTimeField(
        blank=False, null=False, default=timezone.now)
    fk_id_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
