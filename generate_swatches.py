import bpy
import os

# ========== FILAMENT LIST ==========
# Add your filaments here - each entry creates one STL
FILAMENTS = [
    {"colour": "White", "manufacturer": "Bambu Lab", "material": "PLA", "temp_nozzle": "220", "temp_bed": "60"},
    {"colour": "Black", "manufacturer": "Bambu Lab", "material": "PETG", "temp_nozzle": "250", "temp_bed": "80"},
]

# ========== SETTINGS ==========
OUTPUT_FOLDER = "output"  # Folder name for STL files (created next to .blend file)

# Map our fields to Blender text object names
FIELD_MAP = {
    "colour": "TextColour",
    "manufacturer": "TextManufacturer",
    "material": "TextMaterial",
    "temp_nozzle": "TempHotend",
    "temp_bed": "TempBuildplate",
}

# ========== SCRIPT ==========
# Get the folder where the .blend file is saved
blend_dir = os.path.dirname(bpy.data.filepath)
output_dir = os.path.join(blend_dir, OUTPUT_FOLDER)

# Create output folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created folder: {output_dir}")

def export_scene_as_stl(filepath):
    """Convert all objects (including text) to mesh and export as STL"""

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Store original selection and active object
    original_active = bpy.context.view_layer.objects.active

    # Collect all visible objects we want to export
    objects_to_export = []
    for obj in bpy.data.objects:
        if obj.type in ('MESH', 'FONT', 'CURVE') and obj.visible_get():
            objects_to_export.append(obj)

    # Duplicate and convert to mesh
    temp_meshes = []
    for obj in objects_to_export:
        # Select only this object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Duplicate
        bpy.ops.object.duplicate()
        dup = bpy.context.active_object
        dup.name = "TEMP_EXPORT_" + obj.name

        # Convert to mesh if it's text/curve
        if dup.type in ('FONT', 'CURVE'):
            bpy.ops.object.convert(target='MESH')

        temp_meshes.append(bpy.context.active_object)

    # Select all temp meshes for export
    bpy.ops.object.select_all(action='DESELECT')
    for obj in temp_meshes:
        obj.select_set(True)

    if temp_meshes:
        bpy.context.view_layer.objects.active = temp_meshes[0]

    # Export selected objects
    bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True)

    # Delete temp objects
    bpy.ops.object.delete()

    # Restore original active object
    if original_active:
        bpy.context.view_layer.objects.active = original_active

# Generate STL for each filament
print("\n" + "="*40)
print("GENERATING STL FILES")
print("="*40)

for i, filament in enumerate(FILAMENTS):
    # Update each text object
    for field, obj_name in FIELD_MAP.items():
        if obj_name in bpy.data.objects:
            text_obj = bpy.data.objects[obj_name]
            if field == "temp_nozzle":
                text_obj.data.body = filament[field] + "°"
            elif field == "temp_bed":
                text_obj.data.body = filament[field] + "°"
            else:
                text_obj.data.body = filament[field]

    # Force update the scene so text changes take effect
    bpy.context.view_layer.update()

    # Generate filename (sanitize manufacturer name)
    manufacturer_clean = filament['manufacturer'].replace(" ", "")
    filename = f"{manufacturer_clean}_{filament['material']}_{filament['colour']}.stl"
    filepath = os.path.join(output_dir, filename)

    # Export with text converted to mesh
    export_scene_as_stl(filepath)

    print(f"  [{i+1}/{len(FILAMENTS)}] Exported: {filename}")

print("="*40)
print(f"DONE! {len(FILAMENTS)} files saved to: {output_dir}")
print("="*40 + "\n")
