# AnkiHelper

## Requirement

```
python3
BeautifulSoup
selenium
```

## Introduction

The Anki format I used contains 10 different fields:

- id
- word
- plural_variant
- word_type
- pronunciation
- sound
- meaning
- meaning_example
- hint
- image

By default, you can import the **Default.apkg** to anki to get initial deck as well as the format of which. The initiated cards then should be deleted.

On the contrary, you can custom the **dump_to_importable** function in main.py for your own need because it's just the part happening after I've completed crawing data (which is store in ./resource/json)

## Guild 

### Installation

1. Downloading Ankiapp from [Anki](https://apps.ankiweb.net/) and installing according its instructions.

2. Creating profile and importing **Default.apkg** to Anki

3. Dowloading **python, BeautifulSoup, selenium**

### Creating new cards

0. delete **resource** folder as well as current urls in **_urls.txt**

1. Paste the links of vocabularies to the **_urls.txt**


2. Run **main.py**

```
python main.py
```

3. Import the last csv file in **./resource/output** to Anki

4. Copy all files in **./resource/file** to the media location mentioned at [here](https://docs.ankiweb.net/files.html#file-locations)
