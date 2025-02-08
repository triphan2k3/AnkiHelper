from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
import os


class MyHTMLParser:
    def __init__(self, args):
        self.args = args
        self.CAMBRIDGE_PARAMS = {
            "type": "CAMBRIDGE",
            "prefix": "https://dictionary.cambridge.org/dictionary/english/",
            "base_url": "https://dictionary.cambridge.org/dictionary/",
            "subtree": {"class": "pr dictionary"},
            "header": {"class": "pos-header"},
            "uk_pron": [["uk", "dpron-i"], {"type": "audio/mpeg"}, "src"],
            "us_pron": [["us", "dpron-i"], {"type": "audio/mpeg"}, "src"],
            "word_type": "span.pos.dpos",
            "meaning_block": ".def-block.ddef_block",
            "definition_area": ".def.ddef_d.db",
            "example_area": ".examp.dexamp",
            "bold_text": ".lu.dlu",
            "normal_text": ".eg.deg",
            # "ipa": ["region", "pron"],
            "plural": "b.inf",
            "variant": "span.v.dv",
        }
        self.OXFORD_PARAMS = {
            "type": "OXFORD",
            "base_url": "",  # address of oxford is difined
            "subtree": {"id": "main-container"},
            "header": {"class": "top-container"},
            "uk_pron": [["phons_br"], {"class": "pron-uk"}, "data-src-mp3"],
            "us_pron": [["phons_n_am"], {"class": "pron-us"}, "data-src-mp3"],
            "word_type": "span.pos",
            "meaning_block": ".sense",
            "definition_area": ".def",
            "example_area": ".examples li",
            "bold_text": ".cf",
            "normal_text": ".x",
            # "ipa": ['phon'],
            "plural": "span.inflected_form",
            "variant": "span.gram",
        }
        os.makedirs(self.args.json_dir, exist_ok=True)


    def __parse_header(self, subtree, PARAMS) -> list:
        # GET WORD
        header = None
        uk_pron = ""
        us_pron = ""
        uk_ipa = ""
        us_ipa = ""
        word_type = ""
        plural = ""
        variant = ""

        try:
            header = subtree.find(attrs=PARAMS["header"])
            word = header.find(attrs={"class": "headword"}).text
        except Exception:
            # header doesn't exist, nothing to do
            word = subtree.find(attrs={"class": "headword"}).text
            if subtree.select(PARAMS["word_type"]):
                for item in subtree.select(PARAMS["word_type"]):
                    word_type += item.text + "|"
                word_type = list(set(word_type[:-1].split("|")))
                if "phrasal verb" in word_type and "verb" in word_type:
                    word_type.remove("verb")
                word_type = ",".join(word_type)
            # print(uk_pron)
            # print(us_pron)
            # print(word)
            # print(uk_ipa)
            # print(us_ipa)
            return [word, uk_pron, us_pron, uk_ipa, us_ipa, word_type, plural, variant]

        # GET ALTERNATIVE FORMS (plural, variant)
        if header.select(PARAMS["plural"]):
            plural = header.select(PARAMS["plural"])[0].text
        if header.select(PARAMS["variant"]):
            for item in header.select(PARAMS["variant"]):
                variant += item.text + ","
            variant = variant[:-1]

        # GET PRONUNCIATION FILE
        # Find the first audio file for UK pronunciation
        uk_ = header.select("." + ".".join(PARAMS["uk_pron"][0]))
        for item in uk_:
            if item.find(attrs=PARAMS["uk_pron"][1]):
                uk_pron = item.find(attrs=PARAMS["uk_pron"][1]).get(PARAMS["uk_pron"][2])
                uk_pron = urljoin(PARAMS["base_url"], uk_pron)
                break
        # Find the first audio file for US pronunciation
        us_ = header.select("." + ".".join(PARAMS["us_pron"][0]))
        for item in us_:
            if item.find(attrs=PARAMS["us_pron"][1]):
                us_pron = item.find(attrs=PARAMS["us_pron"][1]).get(PARAMS["us_pron"][2])
                us_pron = urljoin(PARAMS["base_url"], us_pron)
                break
        # print(uk_pron)
        # print(us_pron)
        # print(word)

        # GET WORD TYPE
        if subtree.select(PARAMS["word_type"]):
            for item in subtree.select(PARAMS["word_type"]):
                word_type += item.text + "|"
            word_type = ",".join(list(set(word_type[:-1].split("|"))))

        # GET IPA
        if PARAMS["type"] == "OXFORD":
            if header.find(attrs={"class": "collapse"}):
                header.find(attrs={"class": "collapse"}).decompose()

        if PARAMS["type"] == "CAMBRIDGE":
            ipa_blocks = header.find_all(class_=["region", "pron"])
            current_type = "uk"
            for item in ipa_blocks:
                if item.text.lower().startswith("us"):
                    current_type = "us"
                if item.text.lower().startswith("uk"):
                    current_type = "uk"

                if current_type == "uk":
                    uk_ipa += item.text.lower() + " "
                else:
                    us_ipa += item.text.lower() + " "

            uk_ipa = " ".join(uk_ipa.replace("uk", "").split())
            us_ipa = " ".join(us_ipa.replace("us", "").split())
        else:
            uk_ipa_blocks = header.find_all(attrs={"class": "phons_br"})
            us_ipa_blocks = header.find_all(attrs={"class": "phons_n_am"})
            if uk_ipa_blocks:
                for item in uk_ipa_blocks:
                    uk_ipa += item.text + " "
                uk_ipa = " ".join(uk_ipa.replace(",", "").split())
            if us_ipa_blocks:
                for item in us_ipa_blocks:
                    us_ipa += item.text + " "
                us_ipa = " ".join(us_ipa.replace(",", "").split())

            # if uk_:
            #     uk_ipa = uk_[0].text
            #     uk_ipa = " ".join(uk_ipa.replace(",", "").split())
            # if us_:
            #     us_ipa = us_[0].text
            #     us_ipa = " ".join(us_ipa.replace(",", "").split())

        # print(uk_ipa)
        # print(us_ipa)
        return [word, uk_pron, us_pron, uk_ipa, us_ipa, word_type, plural, variant]


    def __parse_meaning(self, subtree, PARAMS) -> list:
        defs = []
        exps = []
        if PARAMS["type"] == "OXFORD":
            if subtree.find(attrs={"class": "idioms"}):
                subtree.find(attrs={"class": "idioms"}).decompose()
        meaning_block = subtree.select(PARAMS["meaning_block"])
        for item in meaning_block:
            # DEFINITION
            definition = item.select(PARAMS["definition_area"])[0].text
            definition = definition.replace(":", "").strip()
            defs.append(definition)
            # print(definition)

            # EXAMPLES
            examples = item.select(PARAMS["example_area"])
            this_block = []
            if examples:
                for example in examples:
                    exp = ""
                    # The bolded text area
                    bold_text = example.select(PARAMS["bold_text"])
                    if bold_text:
                        exp += "<b>" + bold_text[0].text + "</b> "
                        # print("<b>" + bold_text[0].text + "<\\b>", end=" ")
                    # The normal text area
                    normal_text = example.select(PARAMS["normal_text"])
                    if normal_text:
                        exp += normal_text[0].text
                        # print(normal_text[0].text)
                    if exp != "":
                        this_block.append(exp)
            exps.append(this_block)
            # print("=============================================")
        # print(len(defs), len(exps))
        return [defs, exps]


    def __extract_infor(self, file_path):
        PARAMS = {}
        if "CAMBRIDGE" in file_path:
            PARAMS = self.CAMBRIDGE_PARAMS
        else:
            PARAMS = self.OXFORD_PARAMS

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        soup = BeautifulSoup(content, "html.parser")
        subtree = soup.find(attrs=PARAMS["subtree"])

        header_infor = self.__parse_header(subtree, PARAMS)
        word_info = {}
        word_info["id"] = (
            file_path.split("/")[-1]
            .split("\\")[-1]
            .replace(".html", "")
            .replace(self.args.html_filename_deli, "_")
        )
        word_info["word"] = header_infor[0]
        word_info["uk_pron"] = header_infor[1]
        word_info["us_pron"] = header_infor[2]
        word_info["uk_pron_filename"] = (
            "" if not word_info["uk_pron"] else word_info["id"] + "_uk.mp3"
        )
        word_info["us_pron_filename"] = (
            "" if not word_info["us_pron"] else word_info["id"] + "_us.mp3"
        )
        word_info["uk_ipa"] = header_infor[3]
        word_info["us_ipa"] = header_infor[4]
        word_info["word_type"] = header_infor[5]
        word_info["plural"] = header_infor[6]
        word_info["variant"] = header_infor[7]

        meaning_infor = self.__parse_meaning(subtree, PARAMS)
        word_info["definitions"] = meaning_infor[0]
        word_info["examples"] = meaning_infor[1]
        word_list = []
        for item in meaning_infor[1]:
            word_list.extend(item)
        word_info["list_examples"] = word_list
        return word_info

    def parse_html(self, html_file_path, json_file_path):
        """
        Parse content in html_file_path and save to json_file_path
        @param
        - html_file_path: path to html file
        - json_file_path: path to save json file
        """
        word_info = self.__extract_infor(html_file_path)
        with open(json_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(word_info, indent=4, ensure_ascii=False))
        return word_info
