import argparse
from lib.downloader import Downloader
from lib.parsehtml import parse_html
import config
import os
import json
import datetime
from selenium import webdriver


def datetime_str():
    x = datetime.datetime.now()
    return x.strftime("%Y%m%d%H%M%S")


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url-file", type=str, required=False, default=config.URL_FILE)
    parser.add_argument(
        "--download-dir", type=str, default=os.path.join(os.getcwd(), "resource", "file")
    )
    parser.add_argument(
        "--driver", type=str, default="Edge", choices=["Chrome", "Edge", "Safari"]
    )
    parser.add_argument("--storage-dir", type=str, default=config.STORAGE_DIR)
    parser.add_argument("--headless", type=bool, default=True)
    parser.add_argument("--print-mp3", type=bool, default=True)
    parser.add_argument("--filename-file", type=str, default=config.FILENAME_FILE)
    parser.add_argument("--html-dir", type=str, default=config.STORAGE_DIR + "/html")
    parser.add_argument("--json-dir", type=str, default=config.STORAGE_DIR + "/json")
    parser.add_argument(
        "--output-file",
        type=str,
        default=config.STORAGE_DIR + "/output/" + datetime_str() + ".csv",
    )
    parser.add_argument("--html-filename-deli", type=str, default=config.HTML_FILENAME_DELI)
    args = parser.parse_args()
    return args


def dump_to_importable(args):
    os.makedirs(args.storage_dir + "/output", exist_ok=True)
    list_files = os.listdir(args.json_dir)
    with open(args.output_file, "w", encoding='utf-8') as f:
        for file in list_files:
            with open(args.json_dir + "/" + file, "r", encoding='utf-8') as j:
                data = json.load(j)
            elements = []
            elements.append(data["id"])
            elements.append(data["word"])
            # I think only plural or variant can exist at a time
            plural_variant = ""
            if data["plural"]:
                plural_variant += "<i>plural: </i>" + data["plural"] + "|"
            if data["variant"]:
                plural_variant += "<i>variant: </i>" + data["variant"]
            elements.append(plural_variant.replace("|", "\n"))
            # elements.append((data["plural"] + " " + data["variant"]).strip())
            elements[-1] = elements[-1].replace(",", " | ")

            elements.append(data["word_type"].replace(",", " | "))

            pron = ""
            if data["uk_ipa"]:
                pron += "UK " + data["uk_ipa"] + "|"
            if data["us_ipa"]:
                pron += " US " + data["us_ipa"]
            elements.append(pron.replace("|", "\n"))

            sound = ""
            if data["uk_pron_filename"]:
                sound += "UK [sound:" + data["uk_pron_filename"] + "]|"
            if data["us_pron_filename"]:
                sound += " US [sound:" + data["us_pron_filename"] + "]"
            elements.append(sound.replace("|", "\n"))

            elements.append("\n\n".join(data["definitions"]))

            meaning_example = []
            for i in range(len(data["definitions"])):
                next_block = "<b>" + data["definitions"][i] + "</b>\n"
                if len(data["examples"][i]) > 0:
                    next_block += "<ul align='left'>"
                    for item in data["examples"][i]:
                        next_block += "<li>" + item + "</li>"
                    next_block += "</ul>"
                meaning_example.append(next_block)

                # meaning_example.append(
                #     "<b>"
                #     + data["definitions"][i]
                #     + "</b>\n"
                #     + "\n".join(data["examples"][i])
                # )
            elements.append("\n".join(meaning_example))

            elements.append("")
            elements.append("")

            for i in range(len(elements)):
                elements[i] = elements[i].replace('"', '""')
                elements[i] = '"' + elements[i] + '"'

            text = "|".join(elements).replace("\n", "<br>")
            f.write(text + "\n")

if __name__ == "__main__":
    args = set_args()
    driver = webdriver.Chrome()

    f = Downloader(args)

    download_html(args)
    parse_html(args)
    download_file(args)
    dump_to_importable(args)
