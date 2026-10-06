import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from products.models import Product

def delete_dummy_products():
    slugs = [
        'silver-metallic-pen',
        'luxury-leather-notebook',
        'premium-ceramic-mug'
    ]
    
    # Use all_objects to find them even if they were soft-deleted
    products_to_delete = Product.all_objects.filter(slug__in=slugs)
    count = products_to_delete.count()
    
    if count == 0:
        print("No products found with those slugs.")
        return
        
    for p in products_to_delete:
        print(f"Hard deleting: {p.name} (slug: {p.slug})")
        
    # Hard delete from database
    products_to_delete.delete()
    print(f"Successfully deleted {count} products from the database permanently.")

if __name__ == '__main__':
    delete_dummy_products()
