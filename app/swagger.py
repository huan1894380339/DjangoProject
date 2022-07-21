from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                'name': 'user',
                'description': 'Operations about users',
            },
            {
                'name': 'product',
                'description': 'Everything about your products',
            },
            {
                'name': 'cartitem',
                'description': 'Everything about your cartitem',
            },
            {
                'name': 'order',
                'description': 'Access to your orders',
            },
        ]

        return swagger
