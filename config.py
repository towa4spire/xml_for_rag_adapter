XML_FILE = "history.xml" # <-- Change this to your exact dump file name
NS = "{http://www.mediawiki.org/xml/export-0.10/}" #this is the namespace of your xml. typically the link that comes in the header tag

SORTED_FOLDER = "sorted_lore" # this is the folder that will be created in xml_clean_sort.py.
# it will contain txts with the articles' bodies sorted into folders by their categories. you are free to delete categories you find unnecessary
# sorted folder needs to exist before running optional_consolidate.py (run xml_clean_sort.py first)

ORGANIZED_FOLDER = "lore_organized" #this will contain articles with sections consolidated into single files
#so it's more easy to delete a certain article without chasing down all the fragments

FINAL_FOLDER = "lore_organized" #the folder used in to1file.py to create a single txt file with all the articles and respective categories
FOLDERS_TO_EXCLUDE = { #when running to1file, will skip these folders
    "example_folder1",
    "exmaple_folder2"
} 
FINAL_TXT = "lore_dump.txt" #the final txt to be used in RAG