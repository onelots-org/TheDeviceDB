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

    networkTechnologiesList, twoGBands, threeGbands, fourGBands, fiveGBands = network.extract_network(result)
    deviceName, launchYear = launch.extract_network(result)
    metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims = dimensions.extract_network(result)
    displaySpecs, maxRefreshRate, imperialDisplaySize, metricDisplaySizeSquared, widthPixels, heightPixels, displayRatio, displayDensity, displayProtection = display.extract_network(result)
    stockAndroidLaunchVersion, stockAndroidLaunchVersionCodename, stockLaunchRom, stockLaunchRomVersion, chipsetVendor, chipsetCode, chipsetCodename, chipsetMarketName, chipsetEngravingFineness = platform.extract_network(result)

    print(jsonize.jsonize(deviceName,
                     networkTechnologiesList, twoGBands, threeGbands, fourGBands, fiveGBands,
                     launchYear,
                     metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims,
                     displaySpecs, maxRefreshRate, metricDisplaySizeSquared, imperialDisplaySize,
                     widthPixels, heightPixels, displayRatio, displayDensity,
                     stockAndroidLaunchVersion, stockAndroidLaunchVersionCodename, stockLaunchRom, stockLaunchRomVersion,
                     chipsetVendor, chipsetCode, chipsetCodename, chipsetMarketName, chipsetEngravingFineness
                     ))


base_url = ("https://www.gsmarena.com/model-{}.php")
random_page = random.randint(1, 14638)

print(base_url.format(random_page))
get_page(base_url.format(random_page))