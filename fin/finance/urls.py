from django.urls import path
from .views import category_views, home_views, transaction_views, report_views
from django.contrib.auth import views as auth_views


app_name = 'finance'


urlpatterns = [

    path('', home_views.home, name='home'),

    # categories
    # path('categories/', category_views.category_list, name='category_list'),
    path('categories/', category_views.CategoryList.as_view(), name='category_list'),
    path('categories/create/', category_views.category_create, name='category_create'),
    path('categories/<int:pk>/delete/', category_views.category_delete, name='category_delete'),
    path('categories/<int:pk>/update/', category_views.category_update, name='category_update'),

    # transactions
    path('transaction/', transaction_views.TransactionList.as_view(), name='transaction_list'),
    path('transaction/create/', transaction_views.transaction_create, name='transaction_create'),
    path('transaction/<int:pk>/delete/', transaction_views.transaction_delete, name='transaction_delete'),
    path('transaction/<int:pk>/update/', transaction_views.transaction_update, name='transaction_update'),

    # reports
    path('report/', report_views.report, name='report'),

    # account
    path('login/', auth_views.LoginView.as_view(template_name='finance/account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='finance/account/logout.html'), name='logout'),
    path('register/', home_views.register, name='register'),
]
