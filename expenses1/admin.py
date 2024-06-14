from django.contrib import admin
from django.http import HttpRequest
from django.db.models.query import QuerySet
from expenses1.models import TypeCategoryModel, CategoryModel, RecordModel

admin.site.site_header = "Learn Django"
admin.site.site_title = "Django MTV"
admin.site.index_title = "MTV"


# Register your models here.
@admin.register(TypeCategoryModel)
class TypeCategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


# class RecordInline(admin.TabularInline):
#     model = RecordModel
#     extra = 1

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'fk_id_type']
    list_display = ['title', 'fk_id_type']

    # inlines = [RecordInline]

    def normalize_title(self, request: HttpRequest, queryset: QuerySet):
        for category in queryset:
            category.title = category.title.strip().title()
            category.save()

        self.message_user(request, "Normalize title Success!")

    normalize_title.short_description = "Normalize Title"

    actions = ["normalize_title"]


@admin.register(RecordModel)
class RecordAdmin(admin.ModelAdmin):
    fields = ['mount', 'note', 'fk_id_category']
    list_display = ['mount', 'note', 'register_date',
                    'fk_id_category']
