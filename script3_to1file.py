import os
import config

# --- CONFIGURATION ---
# Point this to your folder that still contains the subdirectories
source_dir = config.FINAL_FOLDER
output_file = config.FINAL_TXT

# Add the exact names of the folders you want to completely ignore/exclude
FOLDERS_TO_EXCLUDE = config.FOLDERS_TO_EXCLUDE

print(f"Merging lore files from '{source_dir}' while applying exclusions...")

article_count = 0
excluded_count = 0

# Convert folder names to lowercase for foolproof, case-insensitive matching
exclude_set = {folder.strip().lower() for folder in FOLDERS_TO_EXCLUDE}

with open(output_file, "w", encoding="utf-8") as master:
    # Walk through all subdirectories inside the sorted directory
    for root, dirs, files in os.walk(source_dir):
        # Get the current folder name
        current_folder = os.path.basename(root)
        
        # Check if the current folder is in our exclusion list
        if current_folder.lower() in exclude_set:
            excluded_count += len([f for f in files if f.endswith(".txt")])
            continue  # Skip everything inside this folder
            
        # Process the valid folders
        for filename in sorted(files):
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                    
                    if content:
                        # Write the content followed by a highly distinct marker
                        master.write(content)
                        master.write("\n\n" + "#" * 60 + "\n\n")
                        article_count += 1
                except Exception as e:
                    print(f"Error reading {filename} in {current_folder}: {e}")

print(f"\nSuccess! Merged {article_count} valid lore articles into a single file.")
print(f"Skipped {excluded_count} articles from excluded categories: {', '.join(FOLDERS_TO_EXCLUDE)}")
print(f"Final file size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
