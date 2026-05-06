import json, os

with open('data.json', 'r') as f:
    data = json.load(f)

# Map style name to image filename
photo_map = {
    "Barrel leg jeans":    "images/barrel-leg-jeans.jpg",
    "Linen wide trousers": "images/linen-wide-trousers.jpg",
    "Sheer overlay dress": "images/sheer-overlay-dress.jpg",
    "Coquette aesthetic":  "images/coquette-aesthetic.jpg",
    "Ballet flat":         "images/ballet-flat.jpg",
    "Broderie top":        "images/broderie-top.jpg",
    "Maxi slip dress":     "images/maxi-slip-dress.jpg",
    "Cargo wide leg":      "images/cargo-wide-leg.jpg",
    "Varsity jacket":      "images/varsity-jacket.jpg",
    "Butter yellow set":   "images/butter-yellow-set.jpg",
    "Platform mule":       "images/platform-mule.jpg",
    "Lace trim cami":      "images/lace-trim-cami.jpg",
    "Denim midi skirt":    "images/denim-midi-skirt.jpg",
    "Bubble hem skirt":    "images/bubble-hem-skirt.jpg",
    "Trench coat":         "images/trench-coat.jpg",
    "Ruched sundress":     "images/ruched-sundress.jpg",
    "Mary jane heel":      "images/mary-jane-heel.jpg",
    "Oversized blazer":    "images/oversized-blazer.jpg",
    "Tie-front top":       "images/tie-front-top.jpg",
    "Ribbed tank set":     "images/ribbed-tank-set.jpg",
}

for style in data.get('styles', []):
    name = style.get('name', '')
    if name in photo_map:
        style['photo'] = photo_map[name]
        print(f"Fixed: {name} → {photo_map[name]}")

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done — data.json updated with photo paths")
