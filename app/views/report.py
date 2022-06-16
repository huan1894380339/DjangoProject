from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from app.serializers.report import MonthSerializer, ReportOrderSerializer, ReportOrderSaleSerializer
import numpy as np
import matplotlib.pyplot as plt
from app.utils import PdfConverter


class ReportViewSet(GenericViewSet):
    @action(detail=False, methods=['get'])
    def report_month(self, request):
        serializer = ReportOrderSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        response = (serializer.data)
        pdfc = PdfConverter()
        with open('app/tests/file_tests/report.pdf', 'wb') as pdf_fl:
            pdf_fl.write(pdfc.to_pdf(pdfc.to_html(response)))
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def chart_compare_month(self, request):
        plt.figure(figsize=(16, 15))
        for month in range(1, 13):
            serializer = MonthSerializer(
                month, context={'year': request.query_params.get('year')},
            )
            list_count_by_status = list(
                serializer.data['count_by_status'].values(),
            )
            list_status = tuple(serializer.data['count_by_status'].keys())
            height = list_count_by_status
            bars = list_status
            x_pos = np.arange(len(bars))
            plt.subplot(3, 4, month)
            plt.title('%s%s' % ('Month', month))
            plt.bar(
                x_pos, height, color=[
                    'blue', 'coral', 'green', 'red', 'darkgoldenrod', 'gold',
                ],
            )
            plt.xticks(x_pos, bars)
            plt.xlabel('Status')
        plt.ylabel('Count')
        plt.suptitle('CHART REPORT EVERY MONTH')
        plt.subplots_adjust(
            left=0.125, bottom=0.1, right=0.9,
            top=0.9, wspace=0.2, hspace=0.35,
        )
        plt.savefig('app/tests/file_tests/bar_chart.pdf')
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pie_chart_month(self, request):
        serializer = ReportOrderSaleSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        month = list(serializer.data['total_month'].keys())
        sale = list(serializer.data['total_month'].values())
        ax.pie(sale, labels=month, autopct='%1.2f%%')
        fig.savefig('app/tests/file_tests/pie_chart.pdf')
        return Response(serializer.data)
