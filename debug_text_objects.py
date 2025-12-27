import bpy
import os

# Output file next to the .blend file
blend_dir = os.path.dirname(bpy.data.filepath)
output_file = os.path.join(blend_dir, "debug_output.txt")

lines = []
lines.append("=== DEBUG TEXT OBJECTS ===\n")

# List all text/font objects
lines.append("ALL TEXT OBJECTS FOUND:")
for obj in bpy.data.objects:
    if obj.type == 'FONT':
        lines.append(f"  Name: '{obj.name}' | Text: '{obj.data.body}'")

lines.append("\n--- TESTING WRITES ---")

# Test setting each text object
test_values = {
    "TempNozzle": "999°",
    "TempBuildplate": "888°",
    "TextColour": "TestColour",
    "TextManufacturer": "TestBrand",
    "TextMaterial": "TestMaterial",
}

for obj_name, test_value in test_values.items():
    obj = bpy.data.objects.get(obj_name)
    if obj:
        old_value = obj.data.body
        obj.data.body = test_value
        new_value = obj.data.body
        lines.append(f"  {obj_name}: '{old_value}' -> '{new_value}' (expected: '{test_value}')")
        if new_value != test_value:
            lines.append(f"    ^^^ MISMATCH!")
    else:
        lines.append(f"  {obj_name}: NOT FOUND")

lines.append("\n=== END DEBUG ===")

# Write to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Debug output written to: {output_file}")
