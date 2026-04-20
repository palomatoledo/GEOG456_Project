import json
from collections import defaultdict
import math

# === PARAMETERS ===
INPUT_FILE = "/Users/palomatoledo/Desktop/GEOG 456/Dev/GEOG456/APD_Project/data/stop_pts_with_race_drivers_only.geojson"
OUTPUT_FILE = "/Users/palomatoledo/Desktop/GEOG 456/Dev/GEOG456/APD_Project/output_jittered.geojson"
OFFSET_METERS = 10  # how far to move overlapping points

# Approximate conversion: meters → degrees
def meters_to_degrees(meters, lat):
    return meters / (111320 * math.cos(math.radians(lat)))

# === LOAD DATA ===
with open(INPUT_FILE) as f:
    data = json.load(f)

features = data["features"]

# === STEP 1: Convert single-point MultiPoints → Points ===
for feature in features:
    geom = feature["geometry"]
    if geom["type"] == "MultiPoint" and len(geom["coordinates"]) == 1:
        geom["type"] = "Point"
        geom["coordinates"] = geom["coordinates"][0]

# === STEP 2: Group coordinates ===
# Store (feature_index, sub_index) where sub_index is None for Point
coord_groups = defaultdict(list)

for i, feature in enumerate(features):
    geom = feature["geometry"]

    if geom["type"] == "Point":
        lon, lat = geom["coordinates"]
        coord_groups[(lon, lat)].append((i, None))

    elif geom["type"] == "MultiPoint":
        for k, (lon, lat) in enumerate(geom["coordinates"]):
            coord_groups[(lon, lat)].append((i, k))

# === STEP 3: Apply jitter to duplicates ===
for (lon, lat), entries in coord_groups.items():
    if len(entries) > 1:
        for j, (feature_idx, point_idx) in enumerate(entries):
            angle = (2 * math.pi / len(entries)) * j
            offset_deg = meters_to_degrees(OFFSET_METERS, lat)

            dx = offset_deg * math.cos(angle)
            dy = offset_deg * math.sin(angle)

            new_lon = lon + dx
            new_lat = lat + dy

            geom = features[feature_idx]["geometry"]

            if geom["type"] == "Point":
                geom["coordinates"] = [new_lon, new_lat]

            elif geom["type"] == "MultiPoint":
                geom["coordinates"][point_idx] = [new_lon, new_lat]

# === SAVE OUTPUT ===
with open(OUTPUT_FILE, "w") as f:
    json.dump(data, f)

print(f"Done! Saved to {OUTPUT_FILE}")