import os
import django
import difflib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_images():
    print("Fetching all available images in static/products/...")
    static_products_dir = os.path.join('static', 'products')
    if not os.path.exists(static_products_dir):
        print(f"Error: {static_products_dir} does not exist.")
        return
        
    available_files = os.listdir(static_products_dir)
    
    # Create lower case map for case-insensitive exact matching
    lower_map = {f.lower(): f for f in available_files}
    
    products = Product.objects.all()
    fixed_count = 0
    missing_count = 0
    
    for p in products:
        if not p.image:
            continue
            
        # Expected path like '/static/products/image.png'
        # Convert to local path 'static/products/image.png'
        clean_path = p.image.lstrip('/')
        
        # Windows handles mixed slashes well, but ensure it's normalized for OS
        normalized_path = os.path.normpath(clean_path)
        
        if os.path.exists(normalized_path):
            continue # File exists, no problem
            
        print(f"\nMissing: {p.image} (Product ID: {p.id}, Product: {p.name})")
        
        # Get just the filename
        filename = os.path.basename(clean_path)
        
        # Try 1: Case-insensitive match
        if filename.lower() in lower_map:
            best_match = lower_map[filename.lower()]
            new_image = f"/static/products/{best_match}"
            print(f"  -> Fixed (Case-insensitive match): {new_image}")
            p.image = new_image
            p.save()
            fixed_count += 1
            continue
            
        # Try 2: Different extensions
        base_name = os.path.splitext(filename)[0]
        found_extension = False
        for ext in ['.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG', '.WEBP']:
            test_file = base_name + ext
            if test_file.lower() in lower_map:
                best_match = lower_map[test_file.lower()]
                new_image = f"/static/products/{best_match}"
                print(f"  -> Fixed (Extension changed): {new_image}")
                p.image = new_image
                p.save()
                fixed_count += 1
                found_extension = True
                break
                
        if found_extension:
            continue
            
        # Try 3: Fuzzy matching (e.g. for color mismatches like Black -> Blue)
        # We only want good matches, cutoff=0.7 is a decent threshold
        close_matches = difflib.get_close_matches(filename, available_files, n=1, cutoff=0.7)
        if close_matches:
            best_match = close_matches[0]
            new_image = f"/static/products/{best_match}"
            print(f"  -> Fixed (Fuzzy match): {new_image}")
            p.image = new_image
            p.save()
            fixed_count += 1
            continue
            
        print(f"  -> COULD NOT FIND REPLACEMENT")
        missing_count += 1
        
    print(f"\n--- Summary ---")
    print(f"Fixed: {fixed_count} broken image links.")
    print(f"Still Missing: {missing_count} (Could not find a close enough match in static/products/)")

if __name__ == '__main__':
    fix_images()
