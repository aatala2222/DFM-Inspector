from src.cadquery_feature_extractor import extract_features_from_step

r = extract_features_from_step('C:/Users/aleatala/AppData/Local/Temp/sheet_metal_test.STEP')

print(f"Thickness: {r.get('estimated_min_thickness')}mm")
print(f"Holes: {len(r.get('holes', []))}")

print(f"\nHole-to-Edge distances:")
for d in r.get('hole_to_edge_distances', []):
    print(f"  Hole d={d['hole_diameter']}mm -> min_edge={d['min_edge_distance']}mm")

print(f"\nHole-to-Bend distances (closest per hole):")
for hole in r.get('holes', []):
    dists = [d for d in r.get('hole_to_bend_distances', []) if d['hole_diameter'] == hole['diameter']]
    if dists:
        closest = min(dists, key=lambda x: x['hole_edge_to_bend'])
        print(f"  Hole d={hole['diameter']}mm -> nearest bend: {closest['hole_edge_to_bend']}mm")
