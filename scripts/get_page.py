import cloudscraper
import bs4
import json
import random

scraper = cloudscraper.create_scraper()
with open("headers.json", "r") as f:
    headers_list = json.load(f)

with open("android_versions.json") as f:
    android_codenames = json.load(f)

def get_random_headers():
    return random.choice(headers_list)

def dumpToJson(deviceName,
               networkTechnologiesList,
               twoGBands,
               threeGBands,
               fourGBands,
               fiveGBands,
               launchYear,
               metricDimensions,
               imperialDimensions,
               metricWeight,
               imperialWeight,
               sims,
               displaySpecs,
               maxRefreshRate,
               metricDisplaySizeSquared,
               imperialDisplaySize,
               widthPixels,
               heightPixels,
               displayRatio,
               displayDensity,
               stockAndroidLaunchVersion,
               stockAndroidLaunchVersionCodename,
               stockLaunchRom,
               stockLaunchRomVersion
               ):

    networkTechnologiesList = networkTechnologiesList.text if networkTechnologiesList else "N/A"
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
            "Body": {
                "Dimensions": {
                    "Metric (mm)": metricDimensions,
                    "Imperial (in)": imperialDimensions
                },
                "Weight": {
                    "Metric (g)": metricWeight,
                    "Imperial (oz)": imperialWeight
                },
                "Sim": sims
            },
            "Display": {
                "Specifications": displaySpecs,
                "Max Refresh Rate": maxRefreshRate,
                "Size": {
                    "Inches": imperialDisplaySize,
                    "Square centimeters": metricDisplaySizeSquared
                },
                "Resolution": {
                    "Size": {
                        "Width": widthPixels,
                        "Heigth": heightPixels,
                    },
                    "Ratio": displayRatio,
                    "Density": displayDensity
                },
            },
            "Platform Informations": {
                "OS": {
                    "Android Version": stockAndroidLaunchVersion,
                    "Android Version Codename": stockAndroidLaunchVersionCodename,
                    "Stock OS": stockLaunchRom,
                    "Stock OS Version": stockLaunchRomVersion
                }
            }
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
    dimensions = prettyresult.select_one("[data-spec='dimensions']").text
    weight = prettyresult.select_one("[data-spec='weight']").text
    sims = prettyresult.select_one("[data-spec='sim']").text
    displaySpecsList = prettyresult.select_one("[data-spec='displaytype']").text
    displaySizeList = prettyresult.select_one("[data-spec='displaysize']").text
    displayResolutionList = prettyresult.select_one("[data-spec='displayresolution']").text
    displayProtection = prettyresult.select_one("[data-spec='displayprotection']")
    osInformationsList = prettyresult.select_one("[data-spec='os']")

    # Manipulate dimensions
    metricDimensions, imperialDimensions = dimensions.split("mm")[0].strip(), dimensions.split("(")[1]
    metricDimensions = [float(metric.strip().replace(" ","").replace("mm", "")) for metric in metricDimensions.split("x")]
    imperialDimensions = [float(imperial.strip().replace(" ","").replace("in)", "")) for imperial in imperialDimensions.split("x")]
    # Manipulate weight
    metricWeight, imperialWeight = weight.split("g")[0].strip(), weight.split("(")[1].replace(" lb)", "").replace(" oz)", "")
    # Sim : Yes or N/A
    if "No" in sims:
        sims = "N/A"
    else:
        sims = [sim.strip().replace(" ", "") for sim in sims.split("+")]
    # Display : let's just make a list separated by commas
    displaySpecs = [displaySpecs.strip() for displaySpecs in displaySpecsList.split(",")]
    maxRefreshRate = next((item for item in displaySpecs if "Hz" in item), None)
    # Display Size : returns inches and square cm. Careful, some old devices don't have a display size. Let's return none.
    if "in" not in displaySizeList:
        imperialDisplaySize, metricDisplaySizeSquared = None, None
    else:
        imperialDisplaySize, metricDisplaySizeSquared = displaySizeList.split("inches,")[0].strip().replace(" ", ""), displaySizeList.split("inches,")[1].replace("cm2", " ").split(" (")[0].replace(" ", "")
    # Handling Display Resolution informations. Will show as 0000 x 0000, 00:0 ratio (~000 ppi density) OR just an information (E.g: "5 lines" for nokia 6610)
    if "x" in displayResolutionList:
        if not "ratio" in displayResolutionList:
            widthPixels, heightPixels, displayRatio, displayDensity = displayResolutionList.split(",")[0].split("x")[0].replace(" ", ""), displayResolutionList.split(",")[0].split("x")[1].replace(" ", "").replace("pi","").replace("pixels", ""), "N/A", displayResolutionList.split("(")[1].split("~")[1].split("ppi")[0].strip().replace(" ", "")
        else:
            widthPixels, heightPixels, displayRatio, displayDensity = displayResolutionList.split(",")[0].split("x")[0].replace(" ", ""), displayResolutionList.split(",")[0].split("x")[1].replace(" ", "").replace("pi", ""), displayResolutionList.split(",")[1].split("ratio")[0].strip().replace(" ", ""), displayResolutionList.split(",")[1].split("~")[1].split("ppi")[0].strip().replace(" ", "")
    else:
        widthPixels, heightPixels, displayRatio, displayDensity = "N/A", "N/A", "N/A", displayResolutionList
    # Display protection (Gorilla Glass, etc)
    if not displayProtection:
        displayProtection = "N/A"
    else :
        displayProtection = displayProtection.text
    # OS informations. Come by 3, separated by a comma : Android version, stock rom and its version. Extract all and associate to android codename.
    if not osInformationsList:
        stockAndroidLaunchVersion, stockAndroidLaunchVersionCodename, stockLaunchRom, stockLaunchRomVersion = "N/A", "N/A", "N/A", "N/A"
    else:
        osInformationsList = osInformationsList.text
        stockAndroidLaunchVersion = osInformationsList.split(",")[0].replace("Android ", "") # Not an int !
        stockAndroidLaunchVersionCodename = android_codenames.get(stockAndroidLaunchVersion)
        stockLaunchRom = osInformationsList.split(",")[1].split()[0]
        stockLaunchRomVersion = osInformationsList.split(",")[1].split()[-1]

    print(dumpToJson(deviceName,
                     networkTechnologiesList,
                     twoGBands,
                     threeGBands,
                     fourGBands,
                     fiveGBands,
                     launchYear,
                     metricDimensions,
                     imperialDimensions,
                     metricWeight,
                     imperialWeight,
                     sims,
                     displaySpecs,
                     maxRefreshRate,
                     metricDisplaySizeSquared,
                     imperialDisplaySize,
                     widthPixels,
                     heightPixels,
                     displayRatio,
                     displayDensity,
                     stockAndroidLaunchVersion,
                     stockAndroidLaunchVersionCodename,
                     stockLaunchRom,
                     stockLaunchRomVersion
                     ))


urls = ("https://www.gsmarena.com/xiaomi_redmi_note_11_pro_5g-11333.php",
        "https://www.gsmarena.com/nokia_6110-8.php",
        "https://www.gsmarena.com/oneplus_pad_4-14630.php",
        "https://www.gsmarena.com/oscal_s80-12115.php",
        "https://www.gsmarena.com/i_mobile_319-2595.php"
       )

for url in urls:
    get_page(url)

#get_page("https://www.gsmarena.com/oscal_s80-12115.php")
