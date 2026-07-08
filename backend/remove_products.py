import os
import json
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

slugs_to_remove = [
    'big-top-pen-silver-clip-1972-silver',
    'copper-printed-pot-1931-1'
]

# 1. Remove from customization.json
customization_path = os.path.join('..', 'frontend', 'src', 'data', 'customization.json')
if os.path.exists(customization_path):
    with open(customization_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    initial_count = len(data)
    data = [p for p in data if p.get('id') not in slugs_to_remove]
    final_count = len(data)
    
    with open(customization_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Removed {initial_count - final_count} products from customization.json")
else:
    print(f"customization.json not found at {customization_path}")

# 2. Collect image paths to delete
images_to_check = set()
for slug in slugs_to_remove:
    product = Product.all_objects.filter(slug=slug).first()
    if product:
        if product.image:
            images_to_check.add(product.image)
        if product.image_file:
            images_to_check.add(product.image_file.path)
            
        # Get variant images
        for variant in product.variants.all():
            if variant.image:
                images_to_check.add(variant.image)
            if variant.image_file:
                images_to_check.add(variant.image_file.path)
                
        # Get gallery images
        for img in product.images.all():
            images_to_check.add(img.image.path)
            
        # Delete the product
        product.delete()
        print(f"Deleted product from DB: {slug}")
    else:
        print(f"Product not found in DB: {slug}")

# 3. Check if images are used by other products
images_to_delete = []
for img_path in images_to_check:
    # Very basic check, normally would check all db fields for this path
    # To be safe, we'll only delete files if we are absolutely sure they are unique to this product,
    # but the prompt says "if they are not used by any other product".
    
    # Let's extract the basename to search
    basename = os.path.basename(img_path)
    
    # Check if any other product uses this basename
    is_used = False
    for p in Product.all_objects.all():
        if p.image and basename in p.image:
            is_used = True
            break
        if p.image_file and basename in p.image_file.name:
            is_used = True
            break
            
    if not is_used:
        images_to_delete.append(img_path)

# Delete the images
frontend_public_dir = os.path.join('..', 'frontend', 'public')
for img_path in images_to_delete:
    if os.path.isabs(img_path) and os.path.exists(img_path):
        os.remove(img_path)
        print(f"Deleted image: {img_path}")
    else:
        # Check if it's a relative path in frontend public
        # usually stored as '/static/products/...'
        if img_path.startswith('/'):
            rel_path = img_path[1:]
        else:
            rel_path = img_path
        
        full_path = os.path.join(frontend_public_dir, rel_path)
        # Normalize slashes
        full_path = full_path.replace('/', os.sep).replace('\\', os.sep)
        
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Deleted frontend image: {full_path}")
        else:
            print(f"Could not find image to delete: {img_path} or {full_path}")
