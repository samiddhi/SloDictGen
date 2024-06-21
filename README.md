# SETUP

---

## Python libraries
    for tables:
        icecream
        tqdm
        airium
        pyperclip

    for parsers:
        beautifulsoup4
        openpyxl
        unidecode

    for scraper:
        selenium

    for scoller:
        pyautogui

    for sskj pairing:
        lxml

    translator:
        openai
        python-dotenv
        tiktoken


---
## Files needed:
   - data/[chromedriver.exe](https://chromedriver.chromium.org/downloads)
     - NOTICE: [downgrade chrome](https://www.browserstack.com/guide/downgrade-to-older-versions-of-chrome)
   - data/[Sloleks3.0](https://www.clarin.si/repository/xmlui/handle/11356/1745)/

---
## Multi-step process to generate dictionaries:
   1. Sloleks
      1. Grammar Tables
            - Parse Sloleks3.0 XML files with [`XMLParser`](slo_dict_gen_pkg/parsers.py)
            - Parsed data to HTML with [`Definition`](slo_dict_gen_pkg/formatting.py)
            - lemma+wordform mapping saved as JSON file with [`LemmaFormsParser`](slo_dict_gen_pkg/parsers.py) - [GPT](https://chat.openai.com/share/aef8d7da-ae6b-431b-94ae-4c6bfca90130)
            - Data parsed from XMLs to pickle with [`sloleks_to_pickles`](slo_dict_gen_pkg/parsers.py)
              - can skip this step + save time by modding next step's code
            - Convert pickles to SQLite database with [`SloleksToSQLite`](utils/sqlite_utils.py) - [GPT](https://chatgpt.com/share/d25f1a4e-545d-42d2-87d1-cdcdf5e0eb69)
   2. SSKJ
	  - Scrape SSKJ site (slo & en) with [`Scraper()`](temp_tools/sskj_html_utils.py)
        - If (when) scraping takes multiple attempts (multiple scraped files), combine each language with [`combine_html_files`](temp_tools/combine_files.py)
          - should have en_sskj.html & si_sskj.html in one directory
      - Clean up scraped html with [`HTMLTagRemover()`](temp_tools/sskj_html_utils.py)
      - ~~Pair html \<div class="entry-content"\> elements into JSON with [`PairToJson()`](temp_tools/sskj_html_utils)~~
        - ~~PairToJson assumes the files are identically ordered and will break when a mismatch is encountered. This needs to be manually corrected in the html files.~~
      - Generate SQLite Database for SSKJ Entries by passing [`HTMLParser`](slo_dict_gen_pkg/parsers.py)'s `.sskjentrys` attribute into [`SskjEntrystoSQLite`](slo_dict_gen_pkg/parsers.py)'s `data` arg
        - depricated prerequisite: ~~Parse HTML to pkls with [`HTMLParser`](slo_dict_gen_pkg/parsers.py)'s save_path arg~~
      - Get SSKJ entries into GPT translatable format with [`main_translate_sequence`](temp_tools/translator.py)
        - `_connect` & `_verify` must both be set `False`. 
        - Ensure unique filename
      - Token Minimization:
        - Find most frequently occurring keys with (write) [`get_key_frequencies()`](utils/json_utils.py) & (read) 
          - x

---
### RESOURCES:
   - [Scraping a translated page](https://www.listendata.com/2020/10/translating-web-page-while-scraping.html) ~ *broken* ~
