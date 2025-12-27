#!/usr/bin/env python3
"""
Filament Swatch Manager - Interactive CLI for managing filament profiles.
Run this in terminal: python add_filaments.py
"""

import json
import os

# JSON file location (same folder as this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(SCRIPT_DIR, "filaments.json")


def load_data():
    """Load profiles from JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"profiles": []}


def save_data(data):
    """Save profiles to JSON file."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_profile_name(profile):
    """Generate display name for a profile."""
    return f"{profile['manufacturer']} {profile['material']}"


def list_profiles(data):
    """Display all profiles."""
    if not data['profiles']:
        print("\n  No profiles yet. Add one first!")
        return

    print("\n  Current profiles:")
    print("  " + "-" * 40)
    for i, p in enumerate(data['profiles'], 1):
        colours = ", ".join(p['colours']) if p['colours'] else "(no colours)"
        print(f"  {i}. {get_profile_name(p)}")
        print(f"     Temps: {p['temp_nozzle']}°/{p['temp_bed']}° | Colours: {len(p['colours'])}")
        print(f"     {colours}")
        print()


def add_profile(data):
    """Add a new filament profile."""
    print("\n--- New Profile ---")

    manufacturer = input("Manufacturer: ").strip()
    if not manufacturer:
        print("Cancelled.")
        return

    material = input("Material: ").strip()
    if not material:
        print("Cancelled.")
        return

    temp_nozzle = input("Nozzle temp: ").strip()
    if not temp_nozzle:
        print("Cancelled.")
        return

    temp_bed = input("Bed temp: ").strip()
    if not temp_bed:
        print("Cancelled.")
        return

    colours_input = input("Colours (comma-separated, or leave empty): ").strip()
    colours = [c.strip() for c in colours_input.split(",") if c.strip()] if colours_input else []

    profile = {
        "manufacturer": manufacturer,
        "material": material,
        "temp_nozzle": temp_nozzle,
        "temp_bed": temp_bed,
        "colours": colours
    }

    data['profiles'].append(profile)
    save_data(data)

    print(f"\n✓ Added \"{get_profile_name(profile)}\" with {len(colours)} colour(s)")


def add_colours(data):
    """Add colours to an existing profile."""
    if not data['profiles']:
        print("\n  No profiles yet. Add one first!")
        return

    print("\n--- Add Colours ---")
    print("Select profile:")
    for i, p in enumerate(data['profiles'], 1):
        print(f"  {i}. {get_profile_name(p)} ({len(p['colours'])} colours)")

    try:
        choice = int(input("\nProfile number: ").strip())
        if choice < 1 or choice > len(data['profiles']):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    profile = data['profiles'][choice - 1]

    print(f"\nCurrent colours: {', '.join(profile['colours']) if profile['colours'] else '(none)'}")
    colours_input = input("New colours to add (comma-separated): ").strip()

    if not colours_input:
        print("Cancelled.")
        return

    new_colours = [c.strip() for c in colours_input.split(",") if c.strip()]
    profile['colours'].extend(new_colours)
    save_data(data)

    print(f"\n✓ Added {len(new_colours)} colour(s) to \"{get_profile_name(profile)}\"")
    print(f"  Total colours: {len(profile['colours'])}")


def remove_profile(data):
    """Remove a profile."""
    if not data['profiles']:
        print("\n  No profiles to remove.")
        return

    print("\n--- Remove Profile ---")
    print("Select profile to remove:")
    for i, p in enumerate(data['profiles'], 1):
        print(f"  {i}. {get_profile_name(p)} ({len(p['colours'])} colours)")

    try:
        choice = int(input("\nProfile number (0 to cancel): ").strip())
        if choice == 0:
            print("Cancelled.")
            return
        if choice < 1 or choice > len(data['profiles']):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    profile = data['profiles'].pop(choice - 1)
    save_data(data)

    print(f"\n✓ Removed \"{get_profile_name(profile)}\"")


def remove_colour(data):
    """Remove a colour from a profile."""
    if not data['profiles']:
        print("\n  No profiles yet.")
        return

    print("\n--- Remove Colour ---")
    print("Select profile:")
    for i, p in enumerate(data['profiles'], 1):
        print(f"  {i}. {get_profile_name(p)} ({len(p['colours'])} colours)")

    try:
        choice = int(input("\nProfile number: ").strip())
        if choice < 1 or choice > len(data['profiles']):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    profile = data['profiles'][choice - 1]

    if not profile['colours']:
        print("  No colours in this profile.")
        return

    print(f"\nColours in {get_profile_name(profile)}:")
    for i, c in enumerate(profile['colours'], 1):
        print(f"  {i}. {c}")

    try:
        colour_choice = int(input("\nColour number to remove (0 to cancel): ").strip())
        if colour_choice == 0:
            print("Cancelled.")
            return
        if colour_choice < 1 or colour_choice > len(profile['colours']):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    removed = profile['colours'].pop(colour_choice - 1)
    save_data(data)

    print(f"\n✓ Removed \"{removed}\" from \"{get_profile_name(profile)}\"")


def main():
    """Main menu loop."""
    print("\n" + "=" * 40)
    print("   Filament Swatch Manager")
    print("=" * 40)

    while True:
        data = load_data()

        total_colours = sum(len(p['colours']) for p in data['profiles'])
        print(f"\n[{len(data['profiles'])} profiles, {total_colours} colours total]")

        print("\n1. Add new profile")
        print("2. Add colours to existing profile")
        print("3. List all profiles")
        print("4. Remove a profile")
        print("5. Remove a colour")
        print("6. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            add_profile(data)
        elif choice == "2":
            add_colours(data)
        elif choice == "3":
            list_profiles(data)
        elif choice == "4":
            remove_profile(data)
        elif choice == "5":
            remove_colour(data)
        elif choice == "6":
            print("\nBye! Run generate_swatches.py in Blender to create STLs.\n")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
