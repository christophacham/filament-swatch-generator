# Filament Swatch Card Generator

A Blender script that batch-generates STL files for 3D printable filament swatch cards. Customize the labels (colour, manufacturer, material, temperatures) and export as many variants as you need.

![Filament Swatch Card](https://img.shields.io/badge/Blender-5.0+-orange) ![License](https://img.shields.io/badge/license-MIT-blue)

## What's This For?

When you have multiple filament spools, it's handy to print sample swatch cards with the filament info embossed on them. This script lets you generate STL files for all your filaments at once, instead of manually editing text in Blender for each one.

## Files Included

- `customizable-theultimatefilamentswatch.blend` - The Blender template with editable text objects
- `generate_swatches.py` - Python script to batch-generate STL files
- `FRAMDCN.TTF` - Franklin Gothic Medium Condensed font (required for text display)

## Setup

### 1. Install the Font

The template uses **Franklin Gothic Medium Condensed**. Install it before opening the Blender file:

**Windows:**
- Double-click `FRAMDCN.TTF`
- Click "Install"

**Mac:**
- Double-click `FRAMDCN.TTF`
- Click "Install Font"

**Linux:**
- Copy to `~/.fonts/` or `/usr/share/fonts/`
- Run `fc-cache -fv`

### 2. Open the Template

1. Open Blender (version 4.0 or newer)
2. Open `customizable-theultimatefilamentswatch.blend`

If you still see font errors after installing, go to **Window > Toggle System Console** to dismiss them - they won't affect the export.

## How to Use

### Quick Start

1. Open the `.blend` file in Blender
2. Go to the **Scripting** tab (top menu bar)
3. Click **Open** and select `generate_swatches.py`
4. Edit the `FILAMENTS` list at the top of the script (see below)
5. Click **Run Script** (play button)
6. Find your STL files in the `output/` folder

### Editing the Filament List

Open `generate_swatches.py` and edit the `FILAMENTS` list at the top:

```python
FILAMENTS = [
    {"colour": "White", "manufacturer": "Bambu Lab", "material": "PLA", "temp_nozzle": "220", "temp_bed": "60"},
    {"colour": "Black", "manufacturer": "Bambu Lab", "material": "PETG", "temp_nozzle": "250", "temp_bed": "80"},
    {"colour": "Red", "manufacturer": "Prusa", "material": "ASA", "temp_nozzle": "260", "temp_bed": "100"},
    # Add as many as you want...
]
```

Each entry needs these fields:

| Field | What it is | Examples |
|-------|-----------|----------|
| `colour` | Filament colour | "White", "Matte Black", "Silk Gold" |
| `manufacturer` | Brand name | "Bambu Lab", "Prusa", "Anycubic", "Elegoo" |
| `material` | Material type | "PLA", "PETG", "ABS", "ASA", "TPU" |
| `temp_nozzle` | Nozzle temperature | "220", "250", "260" |
| `temp_bed` | Bed temperature | "60", "80", "100" |

### Output Files

STL files are saved to the `output/` folder with names like:
- `BambuLab_PLA_White.stl`
- `Prusa_ASA_Red.stl`

## Text Objects in the Template

The script modifies these text objects in Blender:

| Object Name | What it shows |
|-------------|---------------|
| `TextColour` | Filament colour |
| `TextManufacturer` | Brand name |
| `TextMaterial` | Material type |
| `TempHotend` | Nozzle temp (adds ° automatically) |
| `TempBuildplate` | Bed temp (adds ° automatically) |

## Troubleshooting

**Text not visible in Blender?**
- Make sure you installed `FRAMDCN.TTF` and restarted Blender

**Empty STL files?**
- Make sure you're using Blender 4.0 or newer
- The script converts text to mesh during export - this is normal

**Script errors?**
- Save the `.blend` file first (the script needs to know the file location)
- Make sure you're in Object Mode, not Edit Mode

## Requirements

- Blender 4.0 or newer (tested on 5.0)
- The included font file installed on your system

## Credits

Based on "The Ultimate Filament Swatch Card" model. Script automation by Christoph Acham.

## License

MIT License - do whatever you want with it.
