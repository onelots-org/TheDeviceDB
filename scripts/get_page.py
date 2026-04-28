import cloudscraper
import bs4
import json
import random

scraper = cloudscraper.create_scraper()
with open("headers.json", "r") as f:
    headers_list = json.load(f)

def get_random_headers():
    return random.choice(headers_list)

def dumpToJson(deviceName,
               networkTechnologiesList,
               twoGBands,
               threeGBands,
               fourGBands,
               fiveGBands,
               launchYear):

    networkTechnologiesList = networkTechnologiesList.text
    twoGBands = twoGBands.text if twoGBands else "N/A"
    threeGBands = threeGBands.text if threeGBands else "N/A"
    fourGBands = fourGBands.text if fourGBands else "N/A"
    fiveGBands = fiveGBands.text if fiveGBands else "N/A"

    if "No cellular connectivity" not in networkTechnologiesList:
        networkTechnologiesList = [tech.strip().replace(" ", "") for tech in networkTechnologiesList.split("/")]
    if "N/A" not in twoGBands:
        twoGBands = [int(twog.strip().replace("GSM", "").replace(" ", "")) for twog in twoGBands.split("/")]
    if "N/A" not in threeGBands and threeGBands:
        threeGBands = [int(threeg.strip().replace("HSDPA", "").replace(" ", "")) for threeg in threeGBands.split("/")]
    if "N/A" not in fourGBands and fourGBands:
        fourGBands = [int(fourg.strip().replace(" ", "")) for fourg in fourGBands.split(",")]
    if "N/A" not in fiveGBands:
        fiveGBands = [int(fiveg.strip().replace("SA/NSA", "").replace(" ", "")) for fiveg in fiveGBands.split(",")]

    page = {
        "Device Name": deviceName,
        "Informations": {
            "Network": {
                "Technologies": networkTechnologiesList,
                "2G Bands": twoGBands,
                "3G Bands": threeGBands,
                "4G Bands": fourGBands,
                "5G Bands": fiveGBands
            },
            "Launch Year": launchYear,
        }
    }
    return page

def get_page(url):
    scraper.headers.update(get_random_headers())
    result = scraper.get(url)
    prettyresult = bs4.BeautifulSoup(result.text, "html.parser")

    deviceName = prettyresult.find("h1").text
    networkTechnologiesList = prettyresult.select_one("[data-spec='nettech']")
    twoGBands = prettyresult.select_one("[data-spec='net2g']")
    threeGBands = prettyresult.select_one("[data-spec='net3g']")
    fourGBands = prettyresult.select_one("[data-spec='net4g']")
    fiveGBands = prettyresult.select_one("[data-spec='net5g']")
    launchYear = prettyresult.select_one("[data-spec='year']").text.split(",")[0].strip()


    print(dumpToJson(deviceName,
                     networkTechnologiesList,
                     twoGBands,
                     threeGBands,
                     fourGBands,
                     fiveGBands,
                     launchYear
                     ))

urls = ("https://www.gsmarena.com/xiaomi_redmi_note_11_pro_5g-11333.php",
        "https://www.gsmarena.com/nokia_6110-8.php",
        "https://www.gsmarena.com/oneplus_pad_4-14630.php",
        "https://www.gsmarena.com/oscal_s80-12115.php",
        "https://www.gsmarena.com/i_mobile_319-2595.php"
       )

for url in urls:
    get_page(url)

