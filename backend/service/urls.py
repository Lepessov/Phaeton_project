from django.urls import path
from . import views

urlpatterns = [
    path('top_purchased/', views.sales_data),
    path('top_purchased_excel/', views.sales_data_excel),


    path('top_searched/', views.top_searched_products),
    path('top_searched_excel/', views.top_searched_products_excel),


    path('low_searches/', views.low_searched_products),
    path('low_searches_excel/', views.low_searched_products_excel),


    path('sales_data_report/', views.sales_data_report),
    path('sales_data_report_excel/', views.sales_data_report_excel),

    path('serched_not_purchased/', views.search_not_purchased_report)


    # path('conv_rate/', views.search_conversion_report)
]