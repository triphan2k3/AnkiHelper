from selenium import webdriver 
import os
import time
  
def create_driver(args, page_load_strategy='eager'):
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

def get_html(driver, url, output_file):
    print("="*100)
    print("PROCESSING: " + url)

    if not url.startswith(("https://dictionary.cambridge.org/", "https://www.oxfordlearnersdictionaries.com/")):
        print("url must be a valid link to a dictionary page, skip downloading html")
        return
    
    if os.path.exists(output_file):
        print("output_file already exists, skip downloading html")
        return    
    print("Entering...") 
    driver.get(url)
    print("Getting content...")
    content = driver.page_source
    with open(output_file, 'w') as f:
        f.write(content)
    print("Done!")

def get_resource(driver, url, output_file, args, delay = 0.3):
    print("="*100)
    print("PROCESSING: " + url)

    if os.path.exists(os.path.join(args.download_dir, output_file)):
        print("output_file already exists, skip downloading file")
        return

    print("Entering...")
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
    print("Done!")

def format_output_file(url, output_file):
    output_file = output_file.replace("-", "_")
    if "cambridge" in url:
        output_file = "CAMBRIDGE|" + output_file
    if "oxford" in url:
        output_file = "OXFORD|" + output_file
    return output_file

def download_html(args):
    # check if url-file is parsed
    if args.url_file is None:
        print("url-file hasn't passed, skip downloading html")
        return
    
    # create driver
    driver = create_driver(args)
    # create html folder
    try:
        os.makedirs(args.html_dir)
        print("directory created")
    except FileExistsError:
        # directory already exists
        print("directory already exists, makedirs skipped")
    
    # process

    with open(args.url_file, 'r') as file:
        for line in file:
            url = line.strip().split("?")[0].strip().split("#")[0].strip()
            output_file = url.split("/")[-1] + ".html"
            output_file = args.html_dir + '/' + format_output_file(url, output_file)
            get_html(driver, url, output_file)

    # close driver
    driver.close()

def download_file(args):
    # check if resource-file is parsed
    if args.filename_file is None:
        print("files-filename hasn't passed, skip downloading resource")
        return
    
    # create driver
    driver = create_driver(args, page_load_strategy='normal')
    # create resource folder
    try:
        os.makedirs(args.download_dir)
        print("directory created")
    except FileExistsError:
        # directory already exists
        print("directory already exists, makedirs skipped")
    
    # process

    with open(args.filename_file, 'r') as file:
        for line in file:
            arr = line.strip().split(" ")
            url = arr[0]
            if len(arr) > 1:
                output_file = arr[1]
            else:
                output_file = url.split("/")[-1]
            get_resource(driver, url, output_file, args)

    # close driver
    driver.close()