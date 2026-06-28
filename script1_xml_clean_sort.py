import os
import re
import config
#from lxml import etree
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
xml_file = config.XML_FILE
output_dir = config.SORTED_FOLDER
NS = config.NS

# Create output folder
os.makedirs(output_dir, exist_ok=True)

print(f"starting streaming through {xml_file}, namespace {NS}, outputting to {output_dir}")

def clean_wiki_text(text):
    """Strips out structural templates and layout code, leaving pure lore."""
    # 1. Strip out complex Infobox/Template blocks
    text = re.sub(r'\{\{[^}]*?\}\}', '', text)
    
    # 2. Fix wiki link brackets [[Phoenix Wright|Phoenix]] -> Phoenix, [[Lawyer]] -> Lawyer
    text = re.sub(r'\[\[([^|\]]+\|)?([^\]]+)\]\]', r'\2', text)
    
    # 3. Completely delete Category syntax lines from the text body
    text = re.sub(r'\[\[Category:[^\]]*?\]\]', '', text, flags=re.IGNORECASE)
    
    # 4. Clean up HTML breaks and custom raw wiki arrow bullets
    text = text.replace('&lt;br&gt;', '\n').replace('&lt;hr/&gt;', '\n').replace('↳', '->')
    text = re.sub(r'<[^>]*?>', '', text)
    
    # 5. Strip bold and italic ticks ('''Phoenix''' -> Phoenix)
    text = text.replace("'''", "").replace("''", "")
    
    # Drop empty code lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

# Stream the file element-by-element using standard ElementTree (ignores the 10MB SAX cap)
context = ET.iterparse(xml_file, events=('end',))

count = 0

for event, elem in context:
    # Ensure we only process the target page elements
    if elem.tag != f'{NS}page':
        continue

    title_elem = elem.find(f'{NS}title')
    ns_elem = elem.find(f'{NS}ns')
    
    # Filter out non-article namespaces (Talk boards, forums, user profiles)
    if ns_elem is not None and ns_elem.text != '0':
        elem.clear()
        continue
        
    if title_elem is not None:
        title = title_elem.text
        
        # Pull ALL revisions available for this page
        revisions = elem.findall(f'{NS}revision')
        if not revisions:
            elem.clear()
            continue
            
        # Target the final element index (-1) to fetch the absolute latest page update
        latest_revision = revisions[-1]
        text_elem = latest_revision.find(f'{NS}text')
        
        if text_elem is not None and text_elem.text:
            raw_text = text_elem.text
            
            # FAST IGNORE: Skip redirect pages completely
            if raw_text.strip().startswith('#REDIRECT') or raw_text.strip().startswith('#redirect'):
                elem.clear()
                continue
            
            # Find the primary category for folder assignments
            categories = re.findall(r'\[\[Category:(.*?)\]\]', raw_text, re.IGNORECASE)
            
            if categories:
                # Discard sort keys (e.g. [[Category:Evidence|3 Zs]] -> Evidence)
                first_cat = categories[0].split('|')[0].strip()
                # Remove punctuation characters to make folder creations completely stable
                category_folder = "".join([c for c in first_cat if c.isalnum() or c in ' _-']).strip()
            else:
                category_folder = "Unsorted"
            
            # Clean the body text using our regex layers
            cleaned_text = clean_wiki_text(raw_text)
            
            # Only save meaningful entries (ignore broken or blank pages)
            if len(cleaned_text) > 20:
                cat_path = os.path.join(output_dir, category_folder)
                os.makedirs(cat_path, exist_ok=True)
                
                # Strip quotation marks or slashes out of the title to keep filesystem happy
                safe_title = "".join([c for c in title if c.isalnum() or c in ' _-']).strip()
                if not safe_title:
                    safe_title = f"article_{count}"
                
                # Write the output file
                with open(os.path.join(cat_path, f"{safe_title}.txt"), "w", encoding="utf-8") as f:
                    f.write(f"ARTICLE TITLE: {title}\n")
                    f.write(f"SECTION: {category_folder}\n")
                    f.write("="*40 + "\n\n")
                    f.write(cleaned_text)
                
                count += 1
                if count % 500 == 0:
                    print(f"processed and sorted {count} lore entries...")

    # Clear elements dynamically to instantly free up your system RAM
    elem.clear()

print(f"\nfinished! processed {count} articles from {xml_file} into '{output_dir}'.")


print(f"\nfinished! processed {count} articles from {xml_file} into '{output_dir}'. you may review the folder and remove undesired folders")
