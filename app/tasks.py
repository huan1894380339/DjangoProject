
from celery import shared_task
from django.core.files import File
from app.models import Product
from pathlib import Path
from app.serializers.product import ImgSerializer
from app.serializers.gallery import GallerySerializer


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 3})
def upload_image_task(self, link_local):
    for i in link_local.get('AnhChinh'):
        product = Product.objects.filter(title=str(Path(i).stem)).first()
        serializer = ImgSerializer(instance=product, data={'path': i})
        serializer.is_valid(raise_exception=True)
        serializer.update(serializer.validated_data, product)
    for i in link_local.get('AnhPhu'):
        product = Product.objects.filter(
            title=str(Path(i).stem).split('_')[0],
        ).first()
        serializer = GallerySerializer(
            data={
                'product': product.id,
                'img_product': File(open(i, 'rb')),
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
