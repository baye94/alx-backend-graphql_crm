# crm/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Product # Assuming Product model is in crm/models.py

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock') # Include fields you want to return

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass # No arguments needed, as it operates on a specific condition

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_list = []
        for product in low_stock_products:
            product.stock += 10 # Increment stock by 10
            product.save()
            updated_list.append(product)

        message = f"Successfully updated {len(updated_list)} low-stock products."
        if not updated_list:
            message = "No low-stock products found to update."

        return UpdateLowStockProducts(updated_products=updated_list, message=message)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
    # Add other mutations here if you have them

schema = graphene.Schema(mutation=Mutation)
# If you have queries, you'd add them to the schema as well:
# class Query(graphene.ObjectType):
#     # Your queries here
#     pass
# schema = graphene.Schema(query=Query, mutation=Mutation)