import json
import re

raw_data = """
Product:
Tik_Tik_Side_Cut_Clip_Pen_2034_Black

Zone:
name-1

x = 518
y = 320
angle = 270
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_U_Clip_Pen_1979_Black

Zone:
name-1

x = 468
y = 618
angle = 282
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_U_Clip_Parker_Rose_gold_Pen_1977

Zone:
name-1

x = 472
y = 578
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_U_Clip_Mettalic_Parker_Pen_1976

Zone:
name-1

x = 486
y = 626
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Touch_Pen_Three_Ring_1962

Zone:
name-1

x = 472
y = 660
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Touch_Pen_Three_Ring_1961

Zone:
name-1

x = 476
y = 642
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Touch_Pen_Single_ring_1966_Black

Zone:
name-1

x = 470
y = 640
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Tik_Tik_Side_Cut_Clip_Pen_2034_Blue

Zone:
name-1

x = 430
y = 604
angle = 303
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_tik_Tik_Rubber_Coated_Pen_1987_Blue

Zone:
name-1

x = 476
y = 666
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_tik_Tik_Rubber_Coated_Pen_1986_Black

Zone:
name-1

x = 470
y = 670
angle = 274
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Tik_Tik_Pen_1984_Black

Zone:
name-1

x = 474
y = 692
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Tik_Tik_Pen_1983

Zone:
name-1

x = 470
y = 670
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Tik_Tik_colourful_Pen_2003_Black

Zone:
name-1

x = 466
y = 656
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_TIE_Shape_Clip_Pen_1981

Zone:
name-1

x = 484
y = 674
angle = 283
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_TIE_Shape_Clip_Pen_1980

Zone:
name-1

x = 454
y = 704
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Structure_Parker_Pen_1974_silver

Zone:
name-1

x = 476
y = 644
angle = 282
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Structure_Parker_Pen_1974_Golden

Zone:
name-1

x = 458
y = 656
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Speed_Pen_2002_Blue

Zone:
name-1

x = 510
y = 500
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Small_Top_Pen_1978_Black

Zone:
name-1

x = 488
y = 652
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Touch_Pen_1985

Zone:
name-1

x = 472
y = 574
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Touch_Pen_1960

Zone:
name-1

x = 474
y = 604
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Touch_Pen_1959

Zone:
name-1

x = 476
y = 626
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------
Product:
RC_Slim_Touch_Pen_1958

Zone:
name-1

x = 484
y = 632
angle = 282
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
C_Slim_Touch_Pen_1957

Zone:
name-1

x = 484
y = 622
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Touch_Pen_1956

Zone:
name-1

x = 478
y = 672
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Touch_Pen_1955

Zone:
name-1

x = 460
y = 662
angle = 284
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Cross_Pen_1968_yellow&silver

Zone:
name-1

x = 464
y = 654
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_Cross_Pen_1968_pink

Zone:
name-1

x = 460
y = 638
angle = 276
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slim_3_Ring_Pen_2005

Zone:
name-1

x = 470
y = 620
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Slender_Gold_Pen_2008

Zone:
name-1

x = 496
y = 626
angle = 277
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Shiny_Black_Pen_2011

Zone:
name-1

x = 474
y = 656
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Round_Top_Pen_2006_Black

Zone:
name-1

x = 480
y = 664
angle = 277
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Retractable_Pen_2003_Black

Zone:
name-1

x = 466
y = 572
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Plane_TOP_Pen_1994_Black

Zone:
name-1

x = 458
y = 646
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Parker_Silver_Clip_Pen_2007_Black

Zone:
name-1

x = 466
y = 660
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Parker_Roller_Pen_1975

Zone:
name-1

x = 470
y = 634
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Parker_Pen_1973

Zone:
name-1

x = 484
y = 620
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Metallic_Balck_Roller_Pen_1988

Zone:
name-1

x = 478
y = 644
angle = 273
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Long_Clip_Pen_2002_Black

Zone:
name-1

x = 490
y = 616
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Leather_Sewing_Pen_2005_Black

Zone:
name-1

x = 512
y = 266
angle = 275
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Leather_Finishing_Pen_1993_Brown

Zone:
name-1

x = 532
y = 284
angle = 282
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Golden_Top_Pen_2004_Pink&Black

Zone:
name-1

x = 514
y = 284
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Golden_Top_Pen_2004_Black

Zone:
name-1

x = 476
y = 614
angle = 276
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Eco_Friendly_Pen_2006

Zone:
name-1

x = 482
y = 528
angle = 282
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------
Product:
RC_Doctor_Silver_Pen_1996

Zone:
name-1

x = 462
y = 638
angle = 283
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Doctor_Golden_Pen_1997

Zone:
name-1

x = 470
y = 608
angle = 282
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Diamond_Golden_Pen_2009_

Zone:
name-1

x = 486
y = 598
angle = 274
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Design_Pen_1991_Black

Zone:
name-1

x = 486
y = 594
angle = 283
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Crock_Pen_1964

Zone:
name-1

x = 490
y = 464
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Colourful_Touch_Pen_1995_Blue

Zone:
name-1

x = 476
y = 682
angle = 284
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
C_Coffee_2_in_1_Pen_1989_

Zone:
name-1

x = 478
y = 548
angle = 284
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_CA_Pen_1999

Zone:
name-1

x = 448
y = 652
angle = 284
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Big_Top_single_Ring_Golden_Pen_1992_

Zone:
name-1

x = 470
y = 630
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Big_Top_Pen_Silver_Clip_1972_Black

Zone:
name-1

x = 452
y = 608
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Big_Top_Pen_Mettalic_Black_1970

Zone:
name-1

x = 480
y = 674
angle = 275
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Big_TOP_Pen_Golden_Clip_1971_Black

Zone:
name-1

x = 468
y = 640
angle = 278
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Big_Top_2_Ring_Pen_1990_Black

Zone:
name-1

x = 480
y = 628
angle = 279
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Big_Clip_Pen_1969

Zone:
name-1

x = 460
y = 670
angle = 280
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Bamboo_Touch_Pen_1963

Zone:
name-1

x = 484
y = 634
angle = 283
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Bamboo_Pen_1967

Zone:
name-1

x = 496
y = 498
angle = 274
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Advocate_Pen_1998

Zone:
name-1

x = 470
y = 632
angle = 285
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
Rc_3_Hole_Pen_1965_Black

Zone:
name-1

x = 476
y = 570
angle = 281
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_12_Pen_1982_Blue

Zone:
name-1

x = 486
y = 570
angle = 286
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Uper_Thick_Body_Gold_Clip_Pen_2012

Zone:
name-1

x = 384
y = 609
angle = 315
maxWidth = 334
height = 72
fontSize = 32

--------------------------------------------------

Product:
RC_Tik_tik_Curve_Pen_2041_Black

Zone:
name-1

x = 636
y = 509
angle = 359
maxWidth = 334
height = 72
fontSize = 32
"""

def normalize(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

def parse_data(text):
    products = {}
    current_product = None
    current_zone = None
    
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('---'):
            continue
        if line.startswith('Product:'):
            current_product = None
            continue
        if current_product is None and not '=' in line and not line.startswith('Zone:'):
            current_product = line
            products[current_product] = {}
            continue
        if line.startswith('Zone:'):
            current_zone = None
            continue
        if current_zone is None and not '=' in line:
            current_zone = line
            products[current_product][current_zone] = {}
            continue
        if '=' in line and current_product and current_zone:
            key, val = line.split('=')
            products[current_product][current_zone][key.strip()] = int(val.strip())
            
    return products

parsed_updates = parse_data(raw_data)
# Create a normalized mapping
normalized_updates = {}
for p_name, zones in parsed_updates.items():
    normalized_updates[normalize(p_name)] = (p_name, zones)

print(f"Parsed {len(parsed_updates)} products to update.")

json_path = r'C:\Users\Shruti\Desktop\SOHAM_GIFT2\Soham_Gift\frontend\src\data\customization.json'

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

updated_slugs = set()

def update_json(node, updates):
    if isinstance(node, list):
        for item in node:
            update_json(item, updates)
    elif isinstance(node, dict):
        slug = node.get('slug')
        if slug and isinstance(slug, str):
            norm_slug = normalize(slug)
            if norm_slug in updates:
                p_name, updates_for_slug = updates[norm_slug]
                
                new_zones = []
                for zone in node.get('zones', []):
                    zone_id = zone.get('id')
                    if zone_id in updates_for_slug:
                        changes = updates_for_slug[zone_id]
                        for k, v in changes.items():
                            zone[k] = v
                        new_zones.append(zone)
                node['zones'] = new_zones
                updated_slugs.add(slug)
        
        # recurse deeper
        for k, v in node.items():
            if isinstance(v, (dict, list)):
                update_json(v, updates)

update_json(config, normalized_updates)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print("Updated slugs:")
for s in updated_slugs:
    print(s)
print(f"Total updated: {len(updated_slugs)}")

# Now print the final zones for verification
def print_updated_zones(node):
    if isinstance(node, list):
        for item in node:
            print_updated_zones(item)
    elif isinstance(node, dict):
        slug = node.get('slug')
        if slug in updated_slugs:
            print(f"Slug: {slug} -> Zones: {[z['id'] for z in node.get('zones', [])]}")
        for k, v in node.items():
            if isinstance(v, (dict, list)):
                print_updated_zones(v)

print_updated_zones(config)

