from django.core.management.base import BaseCommand
from products.models import Product
import random

class Command(BaseCommand):
    help = "Seed product data"

    def handle(self, *args, **options):
        for i in range(20):
            Product.objects.create(
                name=f"Test Product {i+1}",
                price=random.randint(100, 500),
                image="media/products/product-1.png",
                stock=random.randint(1,10),
                priority=random.randint(1,100),
                deleted_at=1

            )
        self.stdout.write(self.style.SUCCESS("Seeded 20 products"))
