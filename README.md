# Filament Swatch Card Generator

A Blender script that batch-generates STL files for 3D printable filament swatch cards. Group your filaments by profile (same temps), add colours, and export STLs for all of them at once.

## What's This For?

When you have multiple filament spools, it helps to print sample swatch cards with the filament info embossed on them. This tool lets you:
- Group filaments by type (e.g., "Bambu Lab PETG HF" with multiple colours)
- Define temperatures once per filament line
- Generate all STL files in one go

## Files Included

- `customizable-theultimatefilamentswatch.blend` - Blender template with editable text
- `add_filaments.py` - Terminal script to manage your filament list
- `generate_swatches.py` - Blender script to create STL files
- `filaments.json` - Your saved filament profiles (auto-created)
- `FRAMDCN.TTF` - Required font file

## Quick Start

### Step 1: Add Your Filaments (Terminal)

Open a terminal/command prompt in this folder and run:

```
python add_filaments.py
```

You'll see a menu:
```
========================================
   Filament Swatch Manager
========================================

[0 profiles, 0 colours total]

1. Add new profile
2. Add colours to existing profile
3. List all profiles
4. Remove a profile
5. Remove a colour
6. Exit

Choice: 1

--- New Profile ---
Manufacturer: Bambu Lab
Material: PETG HF
Nozzle temp: 250
Bed temp: 80
Colours (comma-separated): Black, White, Red

✓ Added "Bambu Lab PETG HF" with 3 colours
```

### Step 2: Generate STLs (Blender)

1. Install the font (`FRAMDCN.TTF`) if you haven't already
2. Open `customizable-theultimatefilamentswatch.blend` in Blender
3. Go to the **Scripting** tab
4. Click **Open** and select `generate_swatches.py`
5. Click **Run Script**
6. Find your STL files in the `output/` folder

## How Profiles Work

Instead of entering temperatures for every single colour, you create **profiles**:

```
Profile: "Bambu Lab PETG HF"
├── Temps: 250°C nozzle / 80°C bed
└── Colours: Black, White, Red, Blue

Profile: "Bambu Lab PLA Basic"
├── Temps: 220°C nozzle / 60°C bed
└── Colours: Jade White, Bambu Green
```

The script generates one STL per colour:
- `BambuLab_PETGHF_Black.stl`
- `BambuLab_PETGHF_White.stl`
- `BambuLab_PLABasic_JadeWhite.stl`
- etc.

## Managing Filaments

Run `python add_filaments.py` anytime to:
- **Add new profile** - New filament type with temps
- **Add colours** - Add more colours to existing profile
- **List profiles** - See everything you've added
- **Remove profile** - Delete a whole filament type
- **Remove colour** - Remove a single colour

Your data is saved to `filaments.json` automatically.

## Font Setup

The template uses **Franklin Gothic Medium Condensed**. Install it before opening Blender:

**Windows:** Double-click `FRAMDCN.TTF` → Install

**Mac:** Double-click `FRAMDCN.TTF` → Install Font

**Linux:** Copy to `~/.fonts/` then run `fc-cache -fv`

## Troubleshooting

**"No filaments found" error?**
- Run `python add_filaments.py` first to add profiles and colours

**Text not visible in Blender?**
- Install `FRAMDCN.TTF` and restart Blender

**Empty STL files?**
- Make sure you're using Blender 4.0 or newer

**Script errors?**
- Save the `.blend` file first (the script needs the file location)
- Make sure you're in Object Mode

## Text Objects in the Template

The script modifies these text objects:

| Object Name | What it shows |
|-------------|---------------|
| `TextColour` | Filament colour |
| `TextManufacturer` | Brand name |
| `TextMaterial` | Material type |
| `TempHotend` | Nozzle temperature |
| `TempBuildplate` | Bed temperature |

## Requirements

- Python 3.x (for the terminal script)
- Blender 4.0 or newer
- The included font file

## Credits

Based on "The Ultimate Filament Swatch Card" model. Script automation by Christoph Acham.

## License

MIT License - do whatever you want with it.
