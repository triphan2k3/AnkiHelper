import unittest
from lib.downloader import Downloader
from lib.parsehtml import MyHTMLParser
import argparse
import config
import os
import datetime
import shutil

def datetime_str():
    x = datetime.datetime.now()
    return x.strftime("%Y%m%d%H%M%S")

def string_of_file_url():
    return "https://dictionary.cambridge.org/media/english/uk_pron/u/ukm/ukmam/ukmammo020.mp3 CAMBRIDGE_manoeuvre_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/m/man/maneu/maneuver.mp3 CAMBRIDGE_manoeuvre_us.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/uk_pron/h/hou/house/house__gb_3.mp3 OXFORD_house_1_uk.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/us_pron/h/hou/house/house__us_1.mp3 OXFORD_house_1_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/u/ukp/ukpre/ukprete005.mp3 CAMBRIDGE_pretentiously_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/u/usp/uspre/uspresu005.mp3 CAMBRIDGE_pretentiously_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/u/ukp/ukpre/ukprete007.mp3 CAMBRIDGE_preternatural_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/u/usp/uspre/uspresu007.mp3 CAMBRIDGE_preternatural_us.mp3\nhttps://dictionary.cambridge.org/vi/media/english/uk_pron/e/epd/epd33/epd33125.mp3 CAMBRIDGE_the_uk.mp3\nhttps://dictionary.cambridge.org/vi/media/english/us_pron/t/the/the_0/the_01_00.mp3 CAMBRIDGE_the_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/c/cdo/cdo03/cdo0318ukpret1115.mp3 CAMBRIDGE_preterit_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/c/cdo/cdo03/cdo0318uspret3862.mp3 CAMBRIDGE_preterit_us.mp3\nhttps://dictionary.cambridge.org/vi/media/english/uk_pron/u/uko/ukove/ukoverw016.mp3 CAMBRIDGE_ox_uk.mp3\nhttps://dictionary.cambridge.org/vi/media/english/us_pron/e/eus/eus75/eus75458.mp3 CAMBRIDGE_ox_us.mp3\nhttps://dictionary.cambridge.org/vi/media/english/uk_pron/u/ukl/uklon/uklonel004.mp3 CAMBRIDGE_long_uk.mp3\nhttps://dictionary.cambridge.org/vi/media/english/us_pron/l/lon/long_/long.mp3 CAMBRIDGE_long_us.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/uk_pron/b/boa/board/boarding_school_1_gb_1.mp3 OXFORD_boarding_school_uk.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/us_pron/b/boa/board/boarding_school_1_us_1.mp3 OXFORD_boarding_school_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/u/ukh/ukhot/ukhotfo023.mp3 CAMBRIDGE_house_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/h/hou/house/house.mp3 CAMBRIDGE_house_us.mp3\nhttps://dictionary.cambridge.org/vi/media/english/uk_pron/u/ukm/ukmer/ukmerce002.mp3 CAMBRIDGE_merchandise_uk.mp3\nhttps://dictionary.cambridge.org/vi/media/english/us_pron/e/eus/eus72/eus72968.mp3 CAMBRIDGE_merchandise_us.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/uk_pron/t/the/the__/the__gb_1.mp3 OXFORD_the_1_uk.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/us_pron/t/the/the__/the__us_1_rr.mp3 OXFORD_the_1_us.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/uk_pron/s/sch/sched/schedule__gb_1.mp3 OXFORD_schedule_1_uk.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/us_pron/s/sch/sched/schedule__us_1_rr.mp3 OXFORD_schedule_1_us.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/uk_pron/p/pla/play_/play__gb_1.mp3 OXFORD_play_1_uk.mp3\nhttps://www.oxfordlearnersdictionaries.com/media/english/us_pron/p/pla/play_/play__us_1.mp3 OXFORD_play_1_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/u/ukp/ukpre/ukprete004.mp3 CAMBRIDGE_pretentious_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/p/pre/prete/pretentious.mp3 CAMBRIDGE_pretentious_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/u/ukp/ukpre/ukprete006.mp3 CAMBRIDGE_pretentiousness_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/u/usp/uspre/uspresu006.mp3 CAMBRIDGE_pretentiousness_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/c/ces/cespu/cespuk000922.mp3 CAMBRIDGE_preterm_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/c/ces/cespu/cespus000922.mp3 CAMBRIDGE_preterm_us.mp3\nhttps://dictionary.cambridge.org/media/english/uk_pron/u/uks/uksch/uksched001.mp3 CAMBRIDGE_schedule_uk.mp3\nhttps://dictionary.cambridge.org/media/english/us_pron/s/sch/sched/schedule.mp3 CAMBRIDGE_schedule_us.mp3\nhttps://dictionary.cambridge.org/vi/media/english/uk_pron/c/cdo/cdo12/cdo124ukcarb0300.mp3 CAMBRIDGE_carbo_loading_uk.mp3\nhttps://dictionary.cambridge.org/vi/media/english/us_pron/c/cdo/cdo12/cdo124uscarb0300.mp3 CAMBRIDGE_carbo_loading_us.mp3"

def expected_html_filenames():
    return [
            "CAMBRIDGE;pretentious.html",
            "CAMBRIDGE;pretentiously.html",
            "CAMBRIDGE;pretentiousness.html",
            "CAMBRIDGE;preterit.html",
            "CAMBRIDGE;preterm.html",
            "CAMBRIDGE;preternatural.html",
            "CAMBRIDGE;jack_of_all_trades_master_of_none.html",
            "OXFORD;house_1.html",
            "OXFORD;boarding_school.html",
            "OXFORD;move_in.html",
            "CAMBRIDGE;schedule.html",
            "CAMBRIDGE;manoeuvre.html",
            "CAMBRIDGE;carbo_loading.html",
            "OXFORD;hang_on.html",
            "OXFORD;schedule_1.html",
            "CAMBRIDGE;merchandise.html",
            "OXFORD;the_1.html",
            "CAMBRIDGE;the.html",
            "CAMBRIDGE;take_on.html",
            "CAMBRIDGE;long.html",
            "CAMBRIDGE;house.html",
            "OXFORD;play_1.html",
        ]

def set_args():
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--url-file", type=str, required=False, default=config.URL_FILE)
        parser.add_argument(
            "--download-dir", type=str, default=os.path.join(os.getcwd(), "resource", "file")
        )
        parser.add_argument(
            "--driver", type=str, default="Chrome", choices=["Chrome", "Edge", "Safari"]
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

class TestDownloader(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDownloader, self).__init__(*args, **kwargs)
        self.args = set_args()
        self.url_list = [
            "https://dictionary.cambridge.org/dictionary/english/pretentious",
            "https://dictionary.cambridge.org/dictionary/english/pretentiously",
            "https://dictionary.cambridge.org/dictionary/english/pretentiousness",
            "https://dictionary.cambridge.org/dictionary/english/preterit",
            "https://dictionary.cambridge.org/dictionary/english/preterm",
            "https://dictionary.cambridge.org/dictionary/english/preternatural",
            "https://dictionary.cambridge.org/dictionary/english/jack-of-all-trades-master-of-none?q=jack-of-all-trades%2C+master+of+none",
            "https://www.oxfordlearnersdictionaries.com/definition/english/house_1?q=house",
            "https://www.oxfordlearnersdictionaries.com/definition/english/boarding-school#boarding_school_topg_1",
            "https://www.oxfordlearnersdictionaries.com/definition/english/move-in#move_pvg_4",
            "https://dictionary.cambridge.org/dictionary/english/schedule",
            "https://dictionary.cambridge.org/dictionary/english/manoeuvre",
            "https://dictionary.cambridge.org/vi/dictionary/english/carbo-loading",
            "https://www.oxfordlearnersdictionaries.com/definition/english/hang-on",
            "https://www.oxfordlearnersdictionaries.com/definition/english/schedule_1?q=schedule",
            "https://dictionary.cambridge.org/vi/dictionary/english/merchandise",
            "https://www.oxfordlearnersdictionaries.com/definition/english/the_1?q=the",
            "https://dictionary.cambridge.org/vi/dictionary/english/the",
            "https://dictionary.cambridge.org/vi/dictionary/english/take-on",
            "https://dictionary.cambridge.org/vi/dictionary/english/long",
            "https://dictionary.cambridge.org/dictionary/english/house",
            "https://www.oxfordlearnersdictionaries.com/definition/english/play_1?q=play",
        ]
        try:
            shutil.rmtree(self.args.storage_dir)
        except FileNotFoundError:
            pass
        self.downloader = Downloader(self.args)

    def test_create_html_filename(self):
        # print("TESTING CREATE_HTML_FILENAME")
        
        for url, expected_html_filename in zip(self.url_list, expected_html_filenames()):
            output_file = self.downloader.create_html_filename(url)
            self.assertEqual(output_file, expected_html_filename)

    def test_get_html(self):
        # print("TESTING GET_HTML")
        # try:
        #     shutil.rmtree(self.args.storage_dir)
        # except FileNotFoundError:
        #     pass

        for url in self.url_list:
            output_file = self.downloader.create_html_filename(url)
            self.downloader.get_html(url)
            self.assertTrue(os.path.exists(os.path.join(self.downloader.args.html_dir, output_file)))

    def test_get_file(self):
        # print("TESTING GET_FILE")
        # try:
        #     shutil.rmtree(self.args.storage_dir)
        # except FileNotFoundError:
        #     pass
        # self.assertFalse(True)
        s = string_of_file_url().split("\n")
        for item in s:
            url, output_file = item.split(" ")
            # output_file = url.replace("/","_").replace(':','_')
            self.downloader.get_mp3(url, output_file)
            # print(url, output_file)
            self.assertTrue(os.path.exists(os.path.join(self.args.download_dir, output_file)))
    
    def test_parse_html(self):
        
        parser = MyHTMLParser(self.args)
        for html_file in expected_html_filenames():
            json_file = html_file.replace(".html", ".json")
            html_file = os.path.join(self.args.html_dir, html_file)
            json_file = os.path.join(self.args.json_dir, json_file)
            parser.parse_html(html_file, json_file)
            self.assertTrue(os.path.exists(json_file))


if __name__ == "__main__":
    unittest.main()
