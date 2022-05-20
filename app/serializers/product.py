import csv
import io

from rest_framework import serializers

from app.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "category",
            "title",
            "description",
            "price",
            "active",
            "img_product",
        ]


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["img_product"]


class CsvSerializer(serializers.Serializer):
    def create(self, validated_data):
        filecsv = validated_data["file"]
        reader = csv.DictReader(io.StringIO(filecsv.read().decode("utf-8")))
        for line in reader:
            Product.objects.create(
                code=line["code"],
                category=Category.objects.get(id=line["category"]),
                description=line["description"],
                title=line["title"],
                price=line["price"],
            )
