from __future__ import annotations

from rest_framework import serializers

from app.models import Gallery


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'product', 'img_product']
