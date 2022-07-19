from drf_yasg.generators import OpenAPISchemaGenerator

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
  def get_schema(self, request=None, public=False):
    """Generate a :class:`.Swagger` object with custom tags"""

    swagger = super().get_schema(request, public)
    swagger.tags = [
        {
            "name": "product",
            "description": "Everything about your products"
        },
        {
            "name": "user",
            "description": "Operations about users"
        },
        {
            "name": "order",
            "description": "Access to your orders"
        },
        {
            "name": "cartitem",
            "description": "Everything about your cartitem"
        },
    ]

    return swagger