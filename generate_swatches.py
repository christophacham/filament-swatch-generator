import bpy
import os
import json

# ========== SETTINGS ==========
OUTPUT_FOLDER = "output"  # Folder name for STL files
JSON_FILE = "filaments.json"  # Filament profiles file

# Map fields to Blender text object names
FIELD_MAP = {
    "colour": "TextColour",
    "manufacturer": "TextManufacturer",
    "material": "TextMaterial",
    "temp_nozzle": "TempHotend",
    "temp_bed": "TempBuildplate",
}

# ========== LOAD FILAMENTS ==========
blend_dir = os.path.dirname(bpy.data.filepath)
json_path = os.path.join(blend_dir, JSON_FILE)
output_dir = os.path.join(blend_dir, OUTPUT_FOLDER)

# Load profiles from JSON
if not os.path.exists(json_path):
    raise FileNotFoundError(f"Filaments file not found: {json_path}\nRun 'python add_filaments.py' first to create profiles.")

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten profiles into individual filament entries
FILAMENTS = []
for profile in data.get('profiles', []):
    for colour in profile.get('colours', []):
        FILAMENTS.append({
            "colour": colour,
            "manufacturer": profile['manufacturer'],
            "material": profile['material'],
            "temp_nozzle": profile['temp_nozzle'],
            "temp_bed": profile['temp_bed'],
        })

if not FILAMENTS:
    raise ValueError("No filaments found! Run 'python add_filaments.py' to add profiles and colours.")

# Create output folder if needed
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created folder: {output_dir}")


def export_scene_as_stl(filepath):
    """Convert all objects (including text) to mesh and export as STL."""

    bpy.ops.object.select_all(action='DESELECT')
    original_active = bpy.context.view_layer.objects.active

    # Collect visible objects
    objects_to_export = []
    for obj in bpy.data.objects:
        if obj.type in ('MESH', 'FONT', 'CURVE') and obj.visible_get():
            objects_to_export.append(obj)

    # Duplicate and convert to mesh
    temp_meshes = []
    for obj in objects_to_export:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        bpy.ops.object.duplicate()
        dup = bpy.context.active_object
        dup.name = "TEMP_EXPORT_" + obj.name

        if dup.type in ('FONT', 'CURVE'):
            bpy.ops.object.convert(target='MESH')

        temp_meshes.append(bpy.context.active_object)

    # Select all temp meshes for export
    bpy.ops.object.select_all(action='DESELECT')
    for obj in temp_meshes:
        obj.select_set(True)

    if temp_meshes:
        bpy.context.view_layer.objects.active = temp_meshes[0]

    # Export
    bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True)

    # Cleanup
    bpy.ops.object.delete()

    if original_active:
        bpy.context.view_layer.objects.active = original_active


# ========== GENERATE STLs ==========
print("\n" + "=" * 40)
print("GENERATING STL FILES")
print(f"Found {len(FILAMENTS)} filament(s) to export")
print("=" * 40)

for i, filament in enumerate(FILAMENTS):
    # Update text objects
    for field, obj_name in FIELD_MAP.items():
        if obj_name in bpy.data.objects:
            text_obj = bpy.data.objects[obj_name]
            value = filament[field]
            if field in ("temp_nozzle", "temp_bed"):
                value = value + "°"
            text_obj.data.body = value

    # Force update
    bpy.context.view_layer.update()

    # Generate filename (sanitize names)
    def sanitize(s):
        return s.replace(" ", "").replace("/", "-")

    manufacturer = sanitize(filament['manufacturer'])
    material = sanitize(filament['material'])
    colour = sanitize(filament['colour'])
    filename = f"{manufacturer}_{material}_{colour}.stl"
    filepath = os.path.join(output_dir, filename)

    # Export
    export_scene_as_stl(filepath)

    print(f"  [{i+1}/{len(FILAMENTS)}] {filename}")

print("=" * 40)
print(f"DONE! {len(FILAMENTS)} files saved to: {output_dir}")
print("=" * 40 + "\n")
