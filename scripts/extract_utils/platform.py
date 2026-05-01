import bs4
import json

with open("resources/android_versions.json") as f:
    android_codenames = json.load(f)

def extract_network(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")

    osInformationsList = prettyresult.select_one("[data-spec='os']")
    chipsetInformationsList = prettyresult.select_one("[data-spec='chipset']")

    # OS informations. Come by 4, separated by a comma : Android version, stock rom and its version. Extract all.
    # stockOsLaunchName = Windows, Android, etc
    # stockOsLaunchVersion = depends on the stockOsLaunchName. for windows, can be 8, 10 etc (10 ?), or for Android... Well yk
    # stockLaunchCustomRom = stock rom, E.g Miui, HyperOs, OxygenOS, etc
    # stockLaunchCustomRomVersion = stock rom version, E.g 10.1, 11, 6 etc... Depends on the "Custom" rom.
    # stockAndroidLaunchCodename = Android codename, disabled if stockOsLaunchName != Android.
    if not osInformationsList:
        stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename = "N/A", "N/A", "N/A", "N/A", "N/A"
    elif "Microsoft" in osInformationsList.text:
        osInformationsList = osInformationsList.text.split(" ")
        stockOsLaunchName = osInformationsList[1].replace(" ", "")
        stockOsLaunchVersion = osInformationsList[2].replace(" ", "")
        stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename = "N/A", "N/A", "N/A"
    elif "Android" in osInformationsList.text:
        osInformationsList = osInformationsList.text
        stockOsLaunchVersion = osInformationsList.split(",")[0].replace("Android ", "")  # Not an int !
        print(stockOsLaunchVersion)
        stockOsLaunchVersionCodename = android_codenames.get(stockOsLaunchVersion)
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

    return stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, chipsetVendor, chipsetCode, chipsetCodename, chipsetMarketName, chipsetEngravingFineness