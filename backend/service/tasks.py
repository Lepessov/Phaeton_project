# from celery import shared_task
# from django.db.models import Sum, Count, Q, F, Case, When
# import pandas as pd
# from django.http import HttpResponse, JsonResponse
#
#
#
# @shared_task
# def generate_excel_file():
#     from service.models import SalesData
#     top_products = SalesData.objects.select_related('product_id', 'client_id') \
#                        .values('product_id__name') \
#                        .annotate(total_quantity=Sum('quantity')) \
#                        .order_by('-total_quantity')[:10]
#
#
#     return excel_output(top_products)
#
#
# def excel_output(query_set):
#     query_set_df = pd.DataFrame.from_records(query_set)
#
#     # Convert the DataFrame to an Excel file
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="excel_output.xlsx"'
#     query_set_df.to_excel(response, index=False)
#
#     return response