from django.urls import path
from . import views


app_name = 'finance'


urlpatterns = [
    # path('categories/', views.category_list, name='category_list'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
]
