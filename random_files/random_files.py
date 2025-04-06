import os
import random
import shutil
import argparse

def copy_random_files(source_dir, output_dir, count):
    """
    Copy a specified number of random files from source directory to output directory.
    
    Args:
        source_dir (str): Path to the source directory
        output_dir (str): Path to the output directory
        count (int): Number of random files to copy
    """
    # Check if directories exist
    if not os.path.isdir(source_dir):
        raise ValueError(f"Source directory '{source_dir}' does not exist.")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all files from source directory (not including subdirectories)
    all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    if not all_files:
        print(f"No files found in source directory '{source_dir}'.")
        return
    
    # Determine how many files to copy (minimum of requested count and available files)
    files_to_copy = min(count, len(all_files))
    
    if files_to_copy < count:
        print(f"Warning: Only {files_to_copy} files available in source directory (requested {count}).")
    
    # Select random files
    selected_files = random.sample(all_files, files_to_copy)
    
    # Copy files
    for file in selected_files:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(output_dir, file)
        
        # Handle name conflicts by adding a suffix
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(file)
            i = 1
            while os.path.exists(dest_path):
                new_name = f"{base}_{i}{ext}"
                dest_path = os.path.join(output_dir, new_name)
                i += 1
        
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {file} to {dest_path}")
    
    print(f"Successfully copied {files_to_copy} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy random files from source to output directory.")
    parser.add_argument("source_dir", help="Source directory path")
    parser.add_argument("output_dir", help="Output directory path")
    parser.add_argument("count", type=int, help="Number of random files to copy")
    
    args = parser.parse_args()
    
    copy_random_files(args.source_dir, args.output_dir, args.count)