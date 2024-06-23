# Hi 👋

I hope you're doing well.

I've left you a bit of a clusterfluff.

Whoops.

### The lowdown:
  - [`insoluble_dregs.json`](/insoluble_dregs.json)
    - the bone scraps after sucking the marrow out of the exported<sup>1</sup> chatGPT responses <sub><sub><sup><sup> - sure, they ~could~ be used for something, but it would torturous manual labor</sup></sub></sub></sup>
  - [`translated_en.json`](/translated_en.json)
    - json loadable GPT responses. <i><b>Not all were exported to [`id_final_trans.json`](/id_final_trans.json)</b></i><sup>2</sup> 
  - [`std_log.json`](/std_log.json)
    - log of ALL chatGPT input objects and output strings
  - [`id_entrytext.json`](/id_entrytext.json)
    - maps each id from [`sskj_entries.db`](/../../db/sskj_entries.db) to corresponding dictionary of text extracted from SSKJ entries' HTML
  - [`unworked.json`](/unworked.json)
    - subset of [`id_entrytext.json`](/id_entrytext.json) that contains every id-entry pair not currently (June 22, 2024) in [`id_final_trans.json`](/id_final_trans.json)
  - [`id_final_trans.json`](/id_final_trans.json)
    - what we've all been waiting for. ChatGPT responses cleaned and JSON'd.
    - You'll need to scan this at some point after it is filled for questionable entries and likely a LOT of polishing --- the inevitably torturous icing on the cake

### General Context
We are creating a reference of dictionaries for each entry in [`sskj_entries.db`](/../../db/sskj_entries.db) for the sake of doing a find and replace of text in the scraped SSKJ HTML blocks so as to (finally) have an english edition of the G.O.A.Ted slovar himself. 

## Footnotes
1.  to [`translated_en.json`](/translated_en.json) if no issues with JSON loading (`json.loads()`) **or** to insoluble.json ([backup](backups/insoluble_original.json)) if there were issues with this. There ARE in fact GPT responses logged in [`std_log.json`](/std_log.json) which will be your job to collect
2. You will likely want to break each GPT response into a list of strings "{...}" with certain criteria (contains comma, colon, backslash, etc) and try to `json.loads()` these dictionary entries individually. You will find `match_successes_to_keys()` & `extract_braces_with_symbols()` in [`translation_cleaner.py`](/../../../temp_tools/translation_cleaner.py) particularly helpful for this task.