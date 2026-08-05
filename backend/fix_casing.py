import os
import sys
import django
import urllib.parse

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_image_casing():
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'products')
    
    if not os.path.exists(static_dir):
        print(f"Error: {static_dir} not found.")
        return
        
    actual_files = os.listdir(static_dir)
    # Create a lower case to exact case mapping
    lower_map = {f.lower(): f for f in actual_files}
    
    products = Product.objects.all()
    mismatch_count = 0
    missing_count = 0
    fixed_count = 0
    
    print(f"Checking {products.count()} products for image casing mismatches in Supabase...")
    
    for p in products:
        if not p.image:
            continue
            
        # Example p.image: '/static/products/Leather USB Drive.jpg'
        db_filename = urllib.parse.unquote(p.image.split('/')[-1])
        
        if db_filename in actual_files:
            # Exact match found, nothing to do
            continue
            
        # If it's not an exact match, check if it's a case mismatch
        if db_filename.lower() in lower_map:
            correct_case_filename = lower_map[db_filename.lower()]
            print(f"Mismatch Found: DB has '{db_filename}', File is '{correct_case_filename}'")
            
            # Fix it!
            new_image_url = f"/static/products/{correct_case_filename}"
            # Keep URL quoting if necessary, but actually in DB it seems we store string as is or unquoted?
            # Let's look at previous scripts, they just do: f"/static/products/{best_match}"
            p.image = f"/static/products/{correct_case_filename}"
            p.save(update_fields=['image'])
            fixed_count += 1
            mismatch_count += 1
        else:
            missing_count += 1
            
    print("\n--- Summary ---")
    print(f"Total Products Checked: {products.count()}")
    print(f"Case Mismatches Fixed: {fixed_count}")
    print(f"Images Not Found in static/products/: {missing_count}")

if __name__ == '__main__':
    fix_image_casing()
