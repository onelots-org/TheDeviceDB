import bs4
import json

with open("resources/android_versions.json") as f:
    android_codenames = json.load(f)

def extract_network(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")

    osInformationsList = prettyresult.select_one("[data-spec='os']")
    chipsetInformationsList = prettyresult.select_one("[data-spec='chipset']")

    # OS informations. Come by 3, separated by a comma : Android version, stock rom and its version. Extract all and associate to android codename.
    if not osInformationsList:
        stockAndroidLaunchVersion, stockAndroidLaunchVersionCodename, stockLaunchRom, stockLaunchRomVersion = "N/A", "N/A", "N/A", "N/A"
    else:
        osInformationsList = osInformationsList.text
        stockAndroidLaunchVersion = osInformationsList.split(",")[0].replace("Android ", "")  # Not an int !
        stockAndroidLaunchVersionCodename = android_codenames.get(stockAndroidLaunchVersion)
        stockLaunchRom = osInformationsList.split(",")[1].split()[0]
        stockLaunchRomVersion = osInformationsList.split(",")[1].split()[-1]
    # Handle chipset infos. Need to take qcom, mtk, unisoc, spreadtrum etc in account.
    if not chipsetInformationsList:
        chipsetVendor, chipsetCode, chipsetCodename, ChipsetMarketName, chipsetEngravingFineness = "N/A", "N/A", "N/A", "N/A", "N/A"
    else:
        chipsetInformationsList = chipsetInformationsList.text
        chipsetVendor = chipsetInformationsList.split()[0]
        chipsetCode = chipsetInformationsList.split()[1]
        if chipsetVendor != "Qualcomm":
            chipsetCodename = "N/A"
        chipsetCodename = "N/A"
        chipsetMarketName = " ".join(chipsetInformationsList.split()[2:-2])
        chipsetEngravingFineness = chipsetInformationsList.split()[-2].replace("(", "")

    return stockAndroidLaunchVersion, stockAndroidLaunchVersionCodename, stockLaunchRom, stockLaunchRomVersion, chipsetVendor, chipsetCode, chipsetCodename, chipsetMarketName, chipsetEngravingFineness