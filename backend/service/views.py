import pandas as pd
from django.db.models import Sum, Count, Q, F, Case, When
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import SalesData, SearchHistory


@api_view(['GET'])
def sales_data(request):
    top_products = SalesData.objects.select_related('product_id', 'client_id') \
                       .values('product_id__name') \
                       .annotate(total_quantity=Sum('quantity')) \
                       .order_by('-total_quantity')[:10]

    top_products_list = list(top_products)

    return JsonResponse(top_products_list, safe=False)


@api_view(['GET'])
def sales_data_excel(request):
    top_products = SalesData.objects.select_related('product_id', 'client_id') \
                       .values('product_id__name') \
                       .annotate(total_quantity=Sum('quantity')) \
                       .order_by('-total_quantity')[:10]

    return excel_output(top_products)


@api_view(['GET'])
def top_searched_products(request):
    top_searches = SearchHistory.objects \
                       .values('search_query') \
                       .annotate(search_count=Count('id')) \
                       .order_by('-search_count')[:10]

    top_searches_list = list(top_searches)
    # Return the list as a JSON response
    return JsonResponse(top_searches_list, safe=False)


@api_view(['GET'])
def top_searched_products_excel(request):
    top_searches = SearchHistory.objects \
                       .values('search_query') \
                       .annotate(search_count=Count('id')) \
                       .order_by('-search_count')[:10]

    return excel_output(top_searches)


@api_view(['GET'])
def low_searched_products(request):
    low_searches = SearchHistory.objects \
                       .values('search_query') \
                       .annotate(search_count=Count('id')) \
                       .order_by('search_count')[:10]

    low_searches_list = list(low_searches)
    # Return the list as a JSON response
    return JsonResponse(low_searches_list, safe=False)


@api_view(['GET'])
def low_searched_products_excel(request):
    low_searches = SearchHistory.objects \
                       .values('search_query') \
                       .annotate(search_count=Count('id')) \
                       .order_by('search_count')[:10]

    return excel_output(low_searches)


@api_view(['GET'])
def sales_data_report(request):

    sales_data = SalesData.objects.select_related('product', 'customer') \
        .values(
        'client_id__city'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum('quantity') * F('product_id__price'),
        total_customers=Count('client_id', distinct=True)
    ).order_by('-total_quantity')

    sales_data_list = list(sales_data)

    return JsonResponse(sales_data_list, safe=False)


@api_view(['GET'])
def sales_data_report_excel(request):

    sales_data = SalesData.objects.select_related('product', 'customer') \
        .values(
        'client_id__city'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum('quantity') * F('product_id__price'),
        total_customers=Count('client_id', distinct=True)
    ).order_by('-total_quantity')

    return excel_output(sales_data)


def excel_output(query_set):
    query_set_df = pd.DataFrame.from_records(query_set)

    # Convert the DataFrame to an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="excel_output.xlsx"'
    query_set_df.to_excel(response, index=False)

    return response


def search_not_purchased_report(request):
    # Get a list of searched items that were not purchased
    not_purchased = SearchHistory.objects.exclude(
        product_id__in=SalesData.objects.values_list('product_id', flat=True)
    ).values('product_id').annotate(
        search_count=Count('id')
    )

    # Get the total number of searches
    total_searches = SearchHistory.objects.count()

    # Calculate the purchase conversion rate for each searched item
    for item in not_purchased:
        item['conversion_rate'] = (
            1 - (item['search_count'] / total_searches)
        ) * 100

    return JsonResponse(list(not_purchased), safe=False)



