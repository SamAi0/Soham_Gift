"""
Migrate product images from local static paths to Supabase Storage URLs.
"""
import os
import sys
import json
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

import django
django.setup()

from django.db import connection
from products.models import Product

# ---------- CONFIG ----------
SUPABASE_PROJECT_REF = 'znyyxbfctmkzflukrmje'
BUCKET_NAME = 'product-images'
SUPABASE_STORAGE_BASE = f'https://{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{BUCKET_NAME}'


def p(msg=''):
    print(msg, flush=True)


def list_storage_objects():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM storage.objects
            WHERE bucket_id = %s AND name IS NOT NULL AND name != ''
            ORDER BY name
        """, [BUCKET_NAME])
        rows = cursor.fetchall()
    return [row[0] for row in rows if row[0] and not row[0].endswith('/')]


def build_public_url(filename):
    encoded = urllib.parse.quote(filename, safe='/')
    return f'{SUPABASE_STORAGE_BASE}/{encoded}'


def extract_filename(path):
    if not path:
        return ''
    if '/' in path:
        return urllib.parse.unquote(path.split('/')[-1])
    return urllib.parse.unquote(path)


def normalize(name):
    name = name.lower().strip()
    for prefix in ['/static/products/', 'static/products/', '/static/', 'static/']:
        if name.startswith(prefix):
            name = name[len(prefix):]
    base = os.path.splitext(name)[0]
    base = base.replace('_', ' ').replace('-', ' ').strip()
    while '  ' in base:
        base = base.replace('  ', ' ')
    return base


def main():
    p("=" * 70)
    p("  SUPABASE STORAGE IMAGE MIGRATION")
    p("=" * 70)
    p()

    # Step 1: List storage files
    p("[1/5] Querying Supabase Storage bucket...")
    storage_names = list_storage_objects()
    p(f"  Found {len(storage_names)} files in '{BUCKET_NAME}' bucket.")
    p()

    # Build lookup maps
    exact_map = {name: name for name in storage_names}
    lower_map = {name.lower(): name for name in storage_names}
    norm_map = {normalize(name): name for name in storage_names}

    # Step 2: Load products
    p("[2/5] Loading all products...")
    products = list(Product.all_objects.all().order_by('id'))
    total = len(products)
    p(f"  Total products: {total}")
    p()

    # Step 3: Match
    p("[3/5] Matching products to storage images...")

    matched = []       # (product, storage_filename, match_type, old_image)
    already_ok = []    # products already pointing to valid Supabase URLs
    unmatched = []     # products we couldn't match

    for prod in products:
        img = prod.image or ''

        # Already correct?
        if img.startswith(SUPABASE_STORAGE_BASE):
            fname = urllib.parse.unquote(img[len(SUPABASE_STORAGE_BASE)+1:])
            if fname in exact_map or fname.lower() in lower_map:
                already_ok.append((prod.id, prod.name, img))
                continue

        filename = extract_filename(img)

        # Exact
        if filename and filename in exact_map:
            matched.append((prod, exact_map[filename], 'exact', img))
            continue

        # Case-insensitive
        if filename and filename.lower() in lower_map:
            matched.append((prod, lower_map[filename.lower()], 'case-insensitive', img))
            continue

        # Normalized
        if filename:
            n = normalize(filename)
            if n and n in norm_map:
                matched.append((prod, norm_map[n], 'normalized', img))
                continue

        # Fuzzy by product name
        pn = normalize(prod.name)
        best = None
        best_score = 0
        for sn in storage_names:
            snn = normalize(sn)
            if pn and snn:
                if pn in snn or snn in pn:
                    score = len(set(pn.split()) & set(snn.split()))
                    if score > best_score:
                        best_score = score
                        best = sn

        if best and best_score >= 2:
            matched.append((prod, best, f'fuzzy({best_score})', img))
            continue

        unmatched.append((prod.id, prod.name, img))

    p(f"  Already correct:  {len(already_ok)}")
    p(f"  New matches:      {len(matched)}")
    p(f"  Unmatched:        {len(unmatched)}")
    p()

    # Step 4: Update DB
    p("[4/5] Updating database records...")
    updated = 0
    errors = []

    for prod, storage_filename, match_type, old_img in matched:
        new_url = build_public_url(storage_filename)
        try:
            prod.image = new_url
            prod.save(update_fields=['image'])
            updated += 1
            if updated % 50 == 0:
                p(f"    ... updated {updated} so far")
        except Exception as e:
            errors.append((prod.id, prod.name, str(e)))

    p(f"  Updated: {updated}")
    if errors:
        p(f"  Errors:  {len(errors)}")
    p()

    # Step 5: Verify
    p("[5/5] Verifying all product image URLs...")
    all_prods = list(Product.all_objects.all().order_by('id'))

    working = []
    broken = []
    no_img = []

    for pr in all_prods:
        if not pr.image:
            no_img.append((pr.id, pr.name))
            continue

        if pr.image.startswith(SUPABASE_STORAGE_BASE):
            fname = urllib.parse.unquote(pr.image[len(SUPABASE_STORAGE_BASE)+1:])
            if fname in exact_map or fname.lower() in lower_map:
                working.append((pr.id, pr.name, pr.image))
            else:
                broken.append((pr.id, pr.name, pr.image, 'Not in storage bucket'))
        elif pr.image.startswith('http'):
            working.append((pr.id, pr.name, pr.image))
        else:
            broken.append((pr.id, pr.name, pr.image, 'Local/static path'))

    # ---------- REPORT ----------
    p()
    p("=" * 70)
    p("  MIGRATION REPORT")
    p("=" * 70)
    p()
    p(f"  Total products:              {total}")
    p(f"  Supabase Storage images:     {len(storage_names)}")
    p(f"  Working image URLs:          {len(working)}")
    p(f"  Broken/missing images:       {len(broken)}")
    p(f"  Products with no image:      {len(no_img)}")
    p(f"  Database records updated:    {updated}")
    p(f"  Already correct (no change): {len(already_ok)}")
    p()

    if broken:
        p("-" * 70)
        p("  BROKEN/MISSING IMAGE URLS:")
        p("-" * 70)
        for pid, pname, pimg, reason in broken[:50]:
            p(f"  ID={pid:<5} | {pname[:45]:<45} | {reason}")
        if len(broken) > 50:
            p(f"  ... and {len(broken)-50} more")
        p()

    if no_img:
        p("-" * 70)
        p("  PRODUCTS WITH NO IMAGE:")
        p("-" * 70)
        for pid, pname in no_img[:30]:
            p(f"  ID={pid:<5} | {pname[:60]}")
        if len(no_img) > 30:
            p(f"  ... and {len(no_img)-30} more")
        p()

    total_issues = len(broken) + len(no_img) + len(errors)
    if total_issues == 0:
        p("  ✅ PRODUCTION TEST: PASS")
    else:
        p(f"  ⚠️  PRODUCTION TEST: {total_issues} issue(s) found")

    p("=" * 70)

    # Save JSON report
    report = {
        'total_products': total,
        'storage_images_found': len(storage_names),
        'working_urls': len(working),
        'broken_missing': len(broken),
        'no_image': len(no_img),
        'records_updated': updated,
        'already_correct': len(already_ok),
        'broken_details': [{'id': pid, 'name': pname, 'url': pimg, 'reason': r} for pid, pname, pimg, r in broken],
        'no_image_details': [{'id': pid, 'name': pname} for pid, pname in no_img],
    }
    rp = os.path.join(os.path.dirname(__file__), 'migration_report.json')
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    p(f"  Report saved: {rp}")


if __name__ == '__main__':
    main()
