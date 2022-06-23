from rest_framework.test import APITestCase
from app.tests.product import ProductFactory
from app.tests.category import CategoryFactory
from app.models import Product
from django.core.files import File
from app.utils import factory_img


class ProductApiTest(APITestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category, active=True)

    def test_get_new_product(self):
        ProductFactory(category=self.category)
        response = self.client.get('/app/api/product/new_product/')
        self.assertEqual(response.status_code, 200)
        product_amount = Product.objects.all().count()
        self.assertEqual(product_amount, 2)

    def test_import_product_csv(self):
        CategoryFactory(title='Shoes')
        CategoryFactory(title='Shirt')
        file = {'file': File(open('app/tests/file_tests/Book1.csv', 'rb'))}
        response = self.client.post(
            '/app/api/product/import_product_csv/', file,
        )
        self.assertEqual(response.status_code, 200)
        product_amount = Product.objects.all().count()
        self.assertEqual(product_amount, 4)

    def test_img_product_from_path(self):
        ProductFactory(title='DKNY Unisex Black', category=self.category)
        ProductFactory(title='DKNY Unisex Black_2', category=self.category)
        path = 'app/tests/file_tests/static/'
        response = self.client.post(
            '/app/api/product/img_product_from_path/', {'path': path},
        )
        self.assertEqual(response.status_code, 200)

    def test_get_list_product_by_category(self):
        category2 = CategoryFactory(title='Shirt')
        ProductFactory(title='DKNY Unisex Black', category=category2)
        response = self.client.get(
            '/app/api/product/list_product_by_category/', {
                'category': 'Shirt',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_add_new_product(self):
        image_file = factory_img()
        category2 = CategoryFactory(title='Shirt')
        new_product = {
            'code': 'SOO1A',
            'category': category2.id,
            'title': 'Shirt 2',
            'description': 'aaa',
            'price': 1000,
            'active': True,
            'img_product': image_file,
        }
        response = self.client.post('/app/api/product/', new_product)
        self.assertEqual(response.status_code, 201)
        new = Product.objects.filter(category=category2).last()
        self.assertEqual(new.title, 'Shirt 2')

    def test_delete_product_success(self):
        count = Product.objects.count()
        response = self.client.delete(f'/app/api/product/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), count - 1)

    def test_update_product_success(self):

        image_file = factory_img()
        self.product.description = 'description before update'
        self.product.img_product = ''
        self.product.save()
        data = {
            'code': 'SOO1A',
            'category': self.category.id,
            'title': 'Shirt 2',
            'description': 'description after update',
            'price': 1000,
            'active': True,
            'img_product': File(image_file),
        }
        response = self.client.put(
            f'/app/api/product/{self.product.id}/', data,
        )
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.code, 'SOO1A')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.description, 'description after update')
        self.assertEqual(self.product.active, True)
        self.assertIsNotNone(self.product.img_product)

    def test_add_new_product_without_default_active(self):
        image_file = factory_img()
        category2 = CategoryFactory(title='Shirt')
        new_product = {
            'code': 'SOO1A',
            'category': category2.id,
            'title': 'Shirt 2',
            'description': 'aaa',
            'price': 10000,
            'active': False,
            'img_product': image_file,
        }

        response = self.client.post('/app/api/product/', new_product)
        newproduct = Product.objects.get(id=response.data['id'])
        self.assertFalse(newproduct.active)
