# RAG text preprocessor

This tool was made to process giant xml files of Wiki dumps. I created it because I needed a way to turn an xml into a compact .txt file for use in RAG in my local LLM instance. 
It's intended to be used with [wikiteam dumps](https://archive.org/search?query=subject%3A%22wikiteam%22 "there are a lot of wiki dumps you can borrow on internet archive!"). I can't tell if it would work well with other xmls. 

## What it does

It reads the last revision of every article and strips out the last revision to put it in .txt. It ignores any non-article content (comments, forum posts, etc). 
It consists of three scripts. 

**Script 1** reads through the `XML_FILE` and puts all articles as .txt files into folders with their respective categories (that's what `SORTED_FOLDER` is for).
> please note that wikis often have wildly inconsistent and mixed category logic. unfortunally you will likely end up with a lot of similar/overlapping/unnecessarily split categories. i have not figured out a simple way to fix it

**Script 2** is optional. It maps out all the files in `SORTED_FOLDER` to look for articles that are sections for the exact same item. This may make it slightly easier to delete certain articles as you won't have to chase down split sections. (that's what `ORGANIZED_FOLDER` is for)

**Script 3** takes all folders and .txt files from `FINAL_FOLDER` and combines them into a single `FINAL_TXT` file. *This is what you can put into your LLM for RAG*

## How to use
>you can try to use it in codespace without downloading the script to your pc, however, due to wikidump xmls typically being huge and the download speed of codespaces being rather slow, it will likely be easier for you to download it onto your pc.
>if you do decide to use codespace (green `<> Code` button near the repo), just skip step 1 and drag-and-drop your file into the codespace or use curl to download the .xml

1. Download `config.py`, `script1`, `script3` and put them in the same folder. script2 is optional.
2. Download your .xml file into the same folder
3. Edit `config.py`
   - have `XML_FILE` variable matching your file's name
   - have `NS` variable matching your dump's namespace (look at the very first parent tag or idk)
   - if you **don't** use **`script2`**, set your `FINAL_FOLDER` same as `SORTED_FOLDER`. if you do, set is the same as `ORGANIZED_FOLDER`
4. Run **script1** (e.g. ```bash python script1_xml_clean_sort.py ``` or just run it through any debugger).
5. Now you can look at the folders inside `SORTED_FOLDER` and delete categories you don't want
6. (optional) Run **script2**. After that you can delete the consolidated files you don't want inside `ORGANIZED_FOLDER`
7. (optional) You can edit `config.py` to list folders contents of which you wish not to see in the final file inside `FOLDERS_TO_EXCLUDE`
8. Run **script3**

DONE! Now in `FINAL_TXT` you will have a single file you can use for RAG. You can safely delete any files you don't intend to use again. Typically this preprocessing turns around a GB of xml for a big fandom wiki into a 5-10mb text file. 

> note: this was vibecoded in like 15 mins with very little edits of my own, so it may have unoptimized logic and stuff. you are free and encouraged to alter the scripts however you want to match your needs.

## Why use a RAG? 

> me personally i was running a really small qwen and it basically had no knowledge of my favorite fandoms. as searching the web would be too expensive for me, i just gave it a RAG feature and stuck the .txt into its database. btw you really should check if your ollama is running the gpu, because it takes an eternity by cpu even if your file is just a couple mb. anyways now im hapi cuz i can ramble about my fav fandoms with the robot bc all the real friends are already exhausted listening to me. Yes hyperfixation's that bad /j 
