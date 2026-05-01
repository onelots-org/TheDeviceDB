import cloudscraper
import json
import random
from extract_utils import network, launch, dimensions, display, platform
from misc import jsonize

scraper = cloudscraper.create_scraper()
with open("resources/headers.json", "r") as f:
    headers_list = json.load(f)


def get_random_headers():
    return random.choice(headers_list)

def get_page(url):
    scraper.headers.update(get_random_headers())
    result = scraper.get(url)

    # Network
    networkTechnologiesList, twoGBands, threeGbands, fourGBands, fiveGBands = network.extract_network(result)
    # Launch
    deviceName, launchYear = launch.extract_network(result)
    # Dimensions
    metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims = dimensions.extract_network(result)
    # Display
    displaySpecs, maxRefreshRate, imperialDisplaySize, metricDisplaySizeSquared, widthPixels, heightPixels, displayRatio, displayDensity, displayProtection = display.extract_network(result)
    # Platform
    stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, maxAndroidVersionUpdate = platform.extract_stockOsInfos(result)
    chipsets = platform.extract_chipsetInfos(result)

    print(jsonize.jsonize(deviceName,
                     networkTechnologiesList, twoGBands, threeGbands, fourGBands, fiveGBands,
                     launchYear,
                     metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims,
                     displaySpecs, maxRefreshRate, metricDisplaySizeSquared, imperialDisplaySize,
                     widthPixels, heightPixels, displayRatio, displayDensity,
                     stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, maxAndroidVersionUpdate,
                     chipsets
                     ))

#base_url = ("https://www.gsmarena.com/model-{}.php")
#random_page = random.randint(2002, 14638)
#print(base_url.format(random_page))
#get_page(base_url.format(random_page))

get_page("https://www.gsmarena.com/samsung_galaxy_tab_s7_fe-10922.php")

#get_page("https://www.gsmarena.com/motorola_razr_ultra_2026-14638.php")
# TODO : this mofo uses INCHES AND NOT IN IN SIZE GRRRR