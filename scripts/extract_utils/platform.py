import bs4
import json
import re

with open("resources/android_versions.json") as f:
    android_codenames = json.load(f)

with open("resources/mediatek_socs.json") as f:
    mediatek_socs = json.load(f)

with open ("resources/qualcomm_socs.json") as f:
    qualcomm_socs = json.load(f)

# 5th attempt to match Gsmarena's freaking unexisting pattern

def get_android_version(osInformationsList):
    parts = osInformationsList.split(",")
    version = re.search(r'[\d.]+', parts[0])
    if version:
        return version.group()
    if not version:
        version = "N/A"

    return version

def get_android_codename(osInformationsList):
    android_codename = android_codenames.get(get_android_version(osInformationsList))
    return android_codename

def get_android_version_update(osInformationsList, stockOsLaunchVersion):
    if "upgradable" in osInformationsList.lower():
        parts = osInformationsList.split(",")
        for part in parts:
            if "upgradable" in part.lower():
                match = re.search(r'[\d.]+', part)
                if match:
                    return match.group()
    elif "upgrades" in osInformationsList.lower():
        parts = osInformationsList.split(",")
        for part in parts:
            if "upgrades" in part.lower():
                match = re.search(r'\d+', part)
                if match:
                    major = int(match.group()) + int(stockOsLaunchVersion.split(".")[0])
                    return str(major)
    return "N/A"

def get_android_custom_rom(osInformationsList):
    stockLaunchCustomRom, stockLaunchCustomRomVersion = "N/A", "N/A"  # Valeur par défaut

    if len(osInformationsList.split(",")) >= 2:
        interesting = osInformationsList.split(",")[-1]
        if "upgradable" not in interesting.lower() and "upgrades" not in interesting.lower():
            stockLaunchCustomRom = " ".join(interesting.split(" ")[:-1]).strip()
            stockLaunchCustomRomVersion = interesting.split(" ")[-1]

    return stockLaunchCustomRom, stockLaunchCustomRomVersion


def get_engraving_fineness(chipsetInformationsList):
    if "nm" in chipsetInformationsList.lower():
        chipsetEngravingFineness = chipsetInformationsList.split()[-2].replace("(", "")
    else:
        chipsetEngravingFineness = "N/A"
    return chipsetEngravingFineness


def extract_stockOsInfos(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")

    osInformationsList = prettyresult.select_one("[data-spec='os']")

    # OS informations. Come by 4, separated by a comma : Android version, stock rom and its version. Extract all.
    # stockOsLaunchName = Windows, Android, etc
    # stockOsLaunchVersion = depends on the stockOsLaunchName. for windows, can be 8, 10 etc (10 ?), or for Android... Well yk
    # stockLaunchCustomRom = stock rom, E.g Miui, HyperOs, OxygenOS, etc
    # stockLaunchCustomRomVersion = stock rom version, E.g 10.1, 11, 6 etc... Depends on the "Custom" rom.
    # stockAndroidLaunchCodename = Android codename, disabled if stockOsLaunchName != Android.
    # And since I'm dumb, integrate the max Android version it can go to (if applicable indeed)
    if "Microsoft" in osInformationsList.text:
        osInformationsList = osInformationsList.text.split(" ")
        stockOsLaunchName = osInformationsList[1].replace(" ", "")
        stockOsLaunchVersion = osInformationsList[2].replace(" ", "")
        stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, maxAndroidVersionUpdate = "N/A", "N/A", "N/A", "N/A"

    elif "Android" in osInformationsList.text:
        osInformationsList = osInformationsList.text
        stockOsLaunchName = "Android"
        stockOsLaunchVersion = get_android_version(osInformationsList)
        stockLaunchCustomRom, stockLaunchCustomRomVersion = get_android_custom_rom(osInformationsList)
        stockAndroidLaunchCodename = get_android_codename(osInformationsList)
        maxAndroidVersionUpdate = get_android_version_update(osInformationsList, stockOsLaunchVersion)

    else:
        stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, maxAndroidVersionUpdate = "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

    return stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, maxAndroidVersionUpdate



def extract_chipsetInfos(page):
    # Handle chipset infos. Need to take qcom, mtk, unisoc, spreadtrum etc in account.
    # In a first time, let's only take care about qcom and mtk.
    td = bs4.BeautifulSoup(page.text, "html.parser").find("td", {"data-spec": "chipset"})
    socs = [part.strip() for part in td.get_text(separator="\n").split("\n") if part.strip()]
    chipsets = []

    for i in range(len(socs)):
        chipsetInformationsList = socs[i].split("-")[0]
        print(chipsetInformationsList)

        if not chipsetInformationsList:
            chipsetVendor, chipsetCode, chipsetCodename, ChipsetMarketName, chipsetEngravingFineness = "N/A", "N/A", "N/A", "N/A", "N/A"
        else:
            chipsetVendor = chipsetInformationsList.split()[0]
            if chipsetVendor == "Qualcomm":
                chipsetCode = chipsetInformationsList.split()[1]
                chipsetCodename = qualcomm_socs.get(chipsetCode)
                if not chipsetCodename:
                    chipsetCodename = "N/A"
                chipsetMarketName = " ".join(chipsetInformationsList.split()[2:-2])
            elif chipsetVendor == "Mediatek":
                chipsetCode = chipsetInformationsList.split()[1]
                chipsetCodename = "N/A"
                if not "MT" in chipsetCode:
                    chipsetMarketName = " ".join(chipsetInformationsList.split()[1:3])
                    chipsetCode = mediatek_socs.get(chipsetMarketName)
                else:
                    chipsetMarketName = " ".join(chipsetInformationsList.split()[2:-2])
            elif chipsetVendor == "Intel":
                chipsetCode = chipsetInformationsList.split()[2]
                chipsetCodename = "N/A"
                chipsetMarketName = " ".join(chipsetInformationsList.split()[1:3])
            elif chipsetVendor == "Exynos":
                if len(chipsetInformationsList.split("(")) == 2:
                    chipsetCodename = "N/A"
                    chipsetCode = "".join(chipsetInformationsList.split()[0:2])
                    chipsetMarketName = " ".join(chipsetInformationsList.split()[0:2])
            else:
                chipsetCodename = "N/A"
                chipsetCode = chipsetInformationsList.split()[1]

        if not "nm" in chipsetInformationsList.lower():
            chipsetEngravingFineness = get_engraving_fineness(chipsetInformationsList)
        else:
            chipsetEngravingFineness = get_engraving_fineness(chipsetInformationsList)

        chipset = {
            "Vendor": chipsetVendor,
            "Platform": chipsetCode,
            "Platform Codename": chipsetCodename,
            "Market Name": chipsetMarketName,
            "Processor Engraving Fineness": chipsetEngravingFineness
        }
        chipsets.append(chipset)

    print(chipsets)
    return chipsets