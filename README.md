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

---
## Files needed:
   - data/[chromedriver.exe](https://chromedriver.chromium.org/downloads)
     - NOTICE: [downgrade chrome](https://www.browserstack.com/guide/downgrade-to-older-versions-of-chrome)
   - data/[Sloleks3.0](https://www.clarin.si/repository/xmlui/handle/11356/1745)/

---
## Multi-step process to generate dictionaries:
   1. Grammar Tables
      - Parse Sloleks3.0 XML files with [XMLParser](slo_dict_gen_pkg/sloleks_parser.py)
	  - Parsed data to HTML with [Definition](slo_dict_gen_pkg/formatting.py)
	  - HTML -> dictionary format with [TBD]()
   2. SSKJ
	  - Scrape SSKJ site (slo & en) with [Scraper](temp_tools/sskj_scraper.py)
      - Clean up scraped html with [HTMLTagRemover](temp_tools/sskj_html_cleaner.py)
      - ~TBD~

---
### RESOURCES:
   - [Scraping a translated page](https://www.listendata.com/2020/10/translating-web-page-while-scraping.html)
