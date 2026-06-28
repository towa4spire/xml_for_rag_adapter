import os
import re
import config

# --- CONFIGURATION ---
source_dir = config.SORTED_FOLDER
output_dir = config.ORGANIZED_FOLDER

os.makedirs(output_dir, exist_ok=True)

# Suffix pattern to find core subjects (e.g., "Phoenix Wright - Biography" -> "Phoenix Wright")
suffix_pattern = re.compile(r'[\s_]*[\(-].*$', re.IGNORECASE)

# Regex to find the SECTION: tag at the beginning of the file
section_pattern = re.compile(r'^SECTION:\s*(.*)$', re.MULTILINE)

# Lightweight structure: { "Core Subject": { "section": "Unsorted", "filepaths": [...] } }
file_map = {}

print(f"mapping out files in {source_dir} for organizing into {output_dir}...")

# 1. First pass: map out sections and categories 
for root, dirs, files in os.walk(source_dir):
    for filename in files:
        if filename.endswith(".txt"):
            base_name = filename[:-4].strip()
            core_subject = suffix_pattern.sub('', base_name).strip().replace('_', ' ')
            
            file_path = os.path.join(root, filename)
            
            # Initialize subject entry if it doesn't exist
            if core_subject not in file_map:
                file_map[core_subject] = {
                    "section": "Unsorted",
                    "filepaths": []
                }
            
            file_map[core_subject]["filepaths"].append(file_path)
            
            # look for the section tag
            if file_map[core_subject]["section"] == "Unsorted":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        head = f.read(1000) # try to find section in first 1k symbols
                    
                    section_match = section_pattern.search(head)
                    if section_match:
                        file_map[core_subject]["section"] = section_match.group(1).strip()
                except Exception as e:
                    print(f"Skipping unreadable file header {filename}: {e}")

print("Consolidating and streaming text files directly to categorized folders...")

# 2. Second pass: Stream and merge text 
saved_count = 0
for subject, data in file_map.items():
    paths = data["filepaths"]
    section_name = data["section"]
    
    # Read and collect content blocks only for this specific subject right now
    blocks = []
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                blocks.append(f.read())
        except Exception as e:
            print(f"Error reading {path}: {e}")
            
    if not blocks:
        continue
        
    # Combine the blocks
    full_profile = f"\n\n{'='*30}\nADDITIONAL SUB-ENTRY DATA\n{'='*30}\n\n".join(blocks)
    
    # Check length condition
    if len(full_profile.strip()) > 50:
        # Sanitize names
        safe_folder_name = "".join([c for c in section_name if c.isalnum() or c in ' _-']).strip()
        safe_filename = "".join([c for c in subject if c.isalnum() or c in ' _-']).strip().replace(' ', '_')
        
        target_folder = os.path.join(output_dir, safe_folder_name)
        os.makedirs(target_folder, exist_ok=True)
        
        # Write to disk, immediately freeing up the memory used by 'full_profile'
        final_path = os.path.join(target_folder, f"{safe_filename}.txt")
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(full_profile)
            
        saved_count += 1
    if saved_count % 300 == 0:
        print(f"processed {saved_count} files...")

print(f"done! successfully consolidated and categorized {saved_count} profiles into {output_dir}. you can now remove undesired articles and run to1file.py")

