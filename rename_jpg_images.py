import os
from pathlib import Path

def rename_jpg_images(folder_path, base_name="david"):
    """
    Rename all .jpg image files in the specified folder with sequential numbering.
    
    Args:
        folder_path: Path to the folder containing images
        base_name: Base name for renamed files (default: "david")
    """
    
    # Convert to Path object
    folder = Path(folder_path)
    
    # Check if folder exists
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist!")
        print("Please create the folder first or check the path.")
        return
    
    # Get all .jpg files in the folder (including .jpeg)
    jpg_files = []
    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg']:
            jpg_files.append(file)
    
    # Sort files by name to ensure consistent ordering
    jpg_files.sort()
    
    if not jpg_files:
        print(f"No .jpg image files found in '{folder_path}'")
        return
    
    print(f"Found {len(jpg_files)} .jpg image(s) to rename.\n")
    print("Current files:")
    for i, file in enumerate(jpg_files, 1):
        print(f"  {i}. {file.name}")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed with renaming? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    print("\nRenaming in progress...\n")
    
    # Rename files
    renamed_count = 0
    for index, file_path in enumerate(jpg_files, start=1):
        # Create new filename with zero-padded number (4 digits)
        new_name = f"{base_name}_{index:04d}.jpg"
        new_path = folder / new_name
        
        # Skip if the file already has the correct name
        if file_path.name == new_name:
            print(f"Skipped: '{file_path.name}' (already has correct name)")
            renamed_count += 1
            continue
        
        # Check if target filename already exists
        if new_path.exists():
            print(f"Warning: '{new_name}' already exists. Skipping '{file_path.name}'")
            continue
        
        try:
            # Rename the file
            file_path.rename(new_path)
            print(f"✓ Renamed: '{file_path.name}' -> '{new_name}'")
            renamed_count += 1
        except Exception as e:
            print(f"✗ Error renaming '{file_path.name}': {e}")
    
    print(f"\n{'=' * 60}")
    print(f"Successfully renamed {renamed_count} out of {len(jpg_files)} image(s).")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    # Get the Documents folder path
    documents_path = Path.home() / "Documents" / "david"
    
    # Alternative: If you want to specify the exact path manually
    # documents_path = r"C:\Users\YourUsername\Documents\david"
    
    print("=" * 60)
    print("JPG Image Renaming Script")
    print("=" * 60)
    print(f"Target folder: {documents_path}")
    print(f"Naming pattern: david_0001.jpg, david_0002.jpg, david_0003.jpg, ...")
    print("=" * 60)
    print()
    
    # Run the renaming function
    rename_jpg_images(documents_path, base_name="david")
    
    print("\nPress Enter to exit...")
    input()
