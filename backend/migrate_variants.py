"""
Migrate product VARIANT images to Supabase Storage URLs.
"""
import os
import sys
import json
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.stdout.reconfigure(line_buffering=True)

import django
django.setup()

from django.db import connection
from products.models import ProductVariant

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
    return urllib.parse.unquote(path.split('/')[-1])


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
    p("  VARIANT IMAGE MIGRATION")
    p("=" * 70)
    p()

    p("[1/4] Querying storage bucket...")
    storage_names = list_storage_objects()
    p(f"  Found {len(storage_names)} files.")
    p()

    exact_map = {name: name for name in storage_names}
    lower_map = {name.lower(): name for name in storage_names}
    norm_map = {normalize(name): name for name in storage_names}

    p("[2/4] Loading variants...")
    variants = list(ProductVariant.objects.all().order_by('id'))
    total = len(variants)
    p(f"  Total variants: {total}")
    p()

    p("[3/4] Matching and updating...")
    updated = 0
    already = 0
    unmatched = []

    for v in variants:
        img = v.image or ''

        if img.startswith(SUPABASE_STORAGE_BASE):
            already += 1
            continue

        filename = extract_filename(img)

        storage_file = None

        if filename and filename in exact_map:
            storage_file = exact_map[filename]
        elif filename and filename.lower() in lower_map:
            storage_file = lower_map[filename.lower()]
        elif filename:
            n = normalize(filename)
            if n and n in norm_map:
                storage_file = norm_map[n]

        if storage_file:
            v.image = build_public_url(storage_file)
            v.save(update_fields=['image'])
            updated += 1
            if updated % 50 == 0:
                p(f"    ... updated {updated}")
        else:
            unmatched.append((v.id, v.product.name if v.product else 'N/A', img))

    p(f"  Already correct: {already}")
    p(f"  Updated: {updated}")
    p(f"  Unmatched: {len(unmatched)}")
    p()

    p("[4/4] Verification...")
    all_v = list(ProductVariant.objects.all())
    working = sum(1 for vv in all_v if vv.image and vv.image.startswith('https://'))
    broken = sum(1 for vv in all_v if vv.image and not vv.image.startswith('https://'))
    no_img = sum(1 for vv in all_v if not vv.image)

    p()
    p("=" * 70)
    p("  VARIANT MIGRATION REPORT")
    p("=" * 70)
    p(f"  Total variants:   {total}")
    p(f"  Working URLs:     {working}")
    p(f"  Still local:      {broken}")
    p(f"  No image:         {no_img}")
    p(f"  Updated:          {updated}")
    p()

    if unmatched:
        p("  UNMATCHED VARIANTS:")
        for vid, pname, vimg in unmatched[:30]:
            p(f"    VID={vid} | {pname[:40]} | {vimg[:60]}")
        if len(unmatched) > 30:
            p(f"    ... and {len(unmatched)-30} more")
        p()

    if broken == 0 and no_img == 0:
        p("  [PASS] All variant images migrated")
    else:
        p(f"  [INFO] {broken + no_img} variants need attention")
    p("=" * 70)


if __name__ == '__main__':
    main()
