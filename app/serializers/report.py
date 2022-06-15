from rest_framework import serializers
from app.models import Order

class MonthSerializer(serializers.Serializer):
    count_order = serializers.SerializerMethodField()
    count_by_status = serializers.SerializerMethodField()
    sale_total_month = serializers.SerializerMethodField()
    def get_count_order(self, month):
        count_order = Order.objects.prefetch_related('orderitem').filter(updated_at__month = month, updated_at__year = self.context['year']).count()
        return count_order
    def get_count_by_status(self, month):
        count_by_status = dict()
        for status in ['NE','CO','SH','RE', 'SU', 'CA']:
            count_new_order = Order.objects.prefetch_related('orderitem').filter(updated_at__month = month, updated_at__year = self.context['year'], status = status).count()
            count_by_status[status] = count_new_order
        return count_by_status
    def get_sale_total_month(self, month):
        sale_total = 0
        orders = Order.objects.prefetch_related('orderitem').filter(updated_at__month = month, updated_at__year = self.context['year'], status__in = ['NE', 'CO', 'SH', 'RE', 'SU'])
        for i in range(0, len(orders)):
            sale_total += orders[i].cart_total
        return sale_total

class ReportOrderSerializer(serializers.Serializer):
    year = serializers.CharField(max_length = 4)
    report_month = serializers.SerializerMethodField()
    count_order = serializers.SerializerMethodField()
    count_by_status = serializers.SerializerMethodField()
    sale_total_year = serializers.SerializerMethodField()

    def validate_year(self, year):
        order = Order.objects.filter(updated_at__year = year)
        if not order:
            raise serializers.ValidationError(f"None value in {year}")
        return year
    def validate_month(self, month):
        if not month:
            raise serializers.ValidationError("None value month")
        return month

    def get_count_order(self, data):
        count_order = Order.objects.filter(updated_at__year = data['year']).count()
        return count_order

    def get_count_by_status(self, data):
        count_by_status = dict()
        for status in ['NE','CO','SH','RE', 'SU', 'CA']:
            count_new_order = Order.objects.filter(updated_at__year = data['year'], status = status).count()
            count_by_status[status] = count_new_order
        return count_by_status


    def get_sale_total_year(self, data):
        sale_total = 0
        orders = Order.objects.filter(updated_at__year = data['year'], status__in = ['NE', 'CO', 'SH', 'RE', 'SU'])
        for i in range(0, len(orders)):
            sale_total += orders[i].cart_total
        return sale_total

    def get_report_month(self, data):
        all_month = dict()
        for month in range(1,13):
            serializer = MonthSerializer(month, context={"year":data['year']})
            all_month[month]= serializer.data
        return all_month


class ReportOrderSaleSerializer(serializers.Serializer):
    year = serializers.CharField(max_length = 4)
    total_month = serializers.SerializerMethodField()
    def get_total_month(self, data):
        list_total_sale_month = dict()
        for month in range(1,13):
            orders = Order.objects.filter(updated_at__month = month, updated_at__year = data['year'])
            total_month = 0
            for i in range(0, len(orders)):
                total_month += orders[i].cart_total
            list_total_sale_month[month]=total_month
        return list_total_sale_month