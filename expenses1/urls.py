from django.urls import path
from django.conf.urls import handler404
from expenses1 import views

urlpatterns = [
    path('', views.index_view, name="home"),
    path('categories/', views.category_view, name="categories"),
    path('records/', views.records_view, name="records"),
    path('delete_category/<int:id_category>',
         views.delete_category_view, name="delete_category"),
    path('delete_record/<int:id_record>',
         views.delete_record_view, name="delete_record"),

    path('update_category/<int:id_category>',
         views.update_category_view, name="update_category"),
    path('update_record/<int:id_record>',
         views.update_record_view, name="update_record"),
    path('historial/', views.historial_view, name="historial")
]

handler404 = 'expenses1.views.custom_404_view'
