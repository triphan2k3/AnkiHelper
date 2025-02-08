from selenium import webdriver 
import os
import time

class Downloader:
    def __init__(self, args):
        self.args = args
        self.html_driver = self.__create_driver(self.args)
        self.mp3_driver = self.__create_driver(self.args, page_load_strategy='normal')
        os.makedirs(self.args.html_dir, exist_ok=True)
        os.makedirs(self.args.download_dir, exist_ok=True)


    def __create_driver(self, args, page_load_strategy='eager'):
        if args.driver != "Chrome" and args.driver != "Edge" and args.driver != "Safari":
            raise ValueError("driver must be 'Chrome' or 'Edge' or 'Safari'")
        
        # create options
        if args.driver == "Chrome":
            options = webdriver.ChromeOptions()
        if args.driver == "Edge":
            options = webdriver.EdgeOptions()
        if args.driver == "Safari":
            options = webdriver.SafariOptions()
        # setup options
        if args.headless:
            options.add_argument('headless')
        options.page_load_strategy = page_load_strategy
        

        if page_load_strategy != 'eager':
            options.add_argument("--mute-audio")
            options.add_experimental_option("prefs", {
                "download.default_directory": args.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True
            })

        # create driver
        if args.driver == "Chrome":
            driver = webdriver.Chrome(options=options)
        if args.driver == "Edge":
            driver = webdriver.Edge(options=options)
        if args.driver == "Safari":
            driver = webdriver.Safari(options=options)
        
        # return created driver
        return driver
    
    def create_html_filename(self, url):
        url = url.strip().split("?")[0].strip().split("#")[0].strip()
        output_file = url.split("/")[-1].replace("-", "_") + ".html"
        if "cambridge" in url:
            output_file = "CAMBRIDGE" + self.args.html_filename_deli + output_file
        if "oxford" in url:
            output_file = "OXFORD" + self.args.html_filename_deli + output_file
        return output_file
    
    def get_html(self, url, output_file=None):
        """
        Download html from url and save to output_file
        @param 
        - url: url to download html
        - output_file: path to save html, use only file name
        """

        

        driver = self.html_driver
        # print("="*100)
        # print("PROCESSING: " + url)

        if not url.startswith(("https://dictionary.cambridge.org/", "https://www.oxfordlearnersdictionaries.com/")):
            print("url must be a valid link to a dictionary page, skip downloading html")
            return
        
        if output_file is None:
            output_file = self.create_html_filename(url)
        output_file = self.args.html_dir + '/' + output_file
        if os.path.exists(output_file):
            # print("output_file already exists, skip downloading html")
            return    
        # print("Entering...") 
        driver.get(url)
        # print("Getting content...")
        content = driver.page_source
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        # print("Done!")

    def get_mp3(self, url, output_file, delay = 0.3):
        """
        Download file from url and save to output_file
        @param
        - driver: webdriver
        - url: url to download resource
        - output_file: path to save resource, use only filename
        - delay: delay time after downloading resource
        """
        

        driver = self.mp3_driver
        # print("="*100)
        # print("PROCESSING: " + url)

        if os.path.exists(os.path.join(self.args.download_dir, output_file)):
            # print("output_file already exists, skip downloading file")
            return

        # print("Entering...")
        driver.get(url)
        script = """
            const link = document.createElement("a");
            link.href = '{url}';
            link.download = '{output_file}';
            document.body.appendChild(link);
            link.click();
        """.format(url=url, output_file=output_file)
        # print(script)
        # return
        driver.execute_script(script)
        time.sleep(delay)
        # with open(output_file, 'wb') as f:
        #     f.write(response.content)
        # print("Done!")
