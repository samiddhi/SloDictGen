# SETUP

---

## Python libraries
    for tables:
        icecream
        tqdm
        airium
        pyperclip

    for parser:
        beautifulsoup4
        openpyxl

    for scraper:
        selenium

    for scoller:
        pyautogui

    for sskj pairing:
        lxml


---
## Files needed:
   - data/[chromedriver.exe](https://chromedriver.chromium.org/downloads)
     - NOTICE: [downgrade chrome](https://www.browserstack.com/guide/downgrade-to-older-versions-of-chrome)
   - data/[Sloleks3.0](https://www.clarin.si/repository/xmlui/handle/11356/1745)/

---
## Multi-step process to generate dictionaries:
   1. Sloleks
      1. Grammar Tables
            - Parse Sloleks3.0 XML files with [XMLParser](slo_dict_gen_pkg/sloleks_parser.py)
            - Parsed data to HTML with [Definition](slo_dict_gen_pkg/formatting.py)
            - lemma+wordform mapping saved as JSON file with [LemmaFormsParser](slo_dict_gen_pkg/sloleks_parser.py) - [GPT](https://chat.openai.com/share/aef8d7da-ae6b-431b-94ae-4c6bfca90130)
   2. SSKJ
	  - Scrape SSKJ site (slo & en) with [Scraper()](temp_tools/sskj_html_utils.py)
        - If (when) scraping takes multiple attempts (multiple scraped files), combine each language with [combine_html_files](temp_tools/combine_files.py)
          - should have en_sskj.html & si_sskj.html in one directory
      - Clean up scraped html with [HTMLTagRemover()](temp_tools/sskj_html_utils.py)
      - Pair html \<div class="entry-content"\> elements into JSON with [PairToJson()](temp_tools/sskj_html_utils)
        - PairToJson assumes the files are identically ordered and will break when a mismatch is encountered. This needs to be manually corrected in the html files.


---
### RESOURCES:
   - [Scraping a translated page](https://www.listendata.com/2020/10/translating-web-page-while-scraping.html) ~ *broken* ~
