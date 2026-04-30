import bs4

def extract_network(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")

    displaySpecsList = prettyresult.select_one("[data-spec='displaytype']").text
    displaySizeList = prettyresult.select_one("[data-spec='displaysize']").text
    displayResolutionList = prettyresult.select_one("[data-spec='displayresolution']").text
    displayProtection = prettyresult.select_one("[data-spec='displayprotection']")

    # Display : let's just make a list separated by commas
    displaySpecs = [displaySpecs.strip() for displaySpecs in displaySpecsList.split(",")]
    maxRefreshRate = next((item for item in displaySpecs if "Hz" in item), None)
    # Display Size : returns inches and square cm. Careful, some old devices don't have a display size. Let's return none.
    if "in" not in displaySizeList:
        imperialDisplaySize, metricDisplaySizeSquared = None, None
    else:
        imperialDisplaySize, metricDisplaySizeSquared = displaySizeList.split("inches,")[0].strip().replace(" ", ""), \
        displaySizeList.split("inches,")[1].replace("cm2", " ").split(" (")[0].replace(" ", "")
    # Handling Display Resolution informations. Will show as 0000 x 0000, 00:0 ratio (~000 ppi density) OR just an information (E.g: "5 lines" for nokia 6610)
    if "x" in displayResolutionList:
        if not "ratio" in displayResolutionList:
            widthPixels, heightPixels, displayRatio, displayDensity = displayResolutionList.split(",")[0].split("x")[
                0].replace(" ", ""), displayResolutionList.split(",")[0].split("x")[1].replace(" ", "").replace("pi",
                                                                                                                "").replace(
                "pixels", ""), "N/A", displayResolutionList.split("(")[1].split("~")[1].split("ppi")[0].strip().replace(
                " ", "")
        else:
            widthPixels, heightPixels, displayRatio, displayDensity = displayResolutionList.split(",")[0].split("x")[
                0].replace(" ", ""), displayResolutionList.split(",")[0].split("x")[1].replace(" ", "").replace("pi",
                                                                                                                ""), \
            displayResolutionList.split(",")[1].split("ratio")[0].strip().replace(" ", ""), \
            displayResolutionList.split(",")[1].split("~")[1].split("ppi")[0].strip().replace(" ", "")
    else:
        widthPixels, heightPixels, displayRatio, displayDensity = "N/A", "N/A", "N/A", displayResolutionList
    # Display protection (Gorilla Glass, etc)
    if not displayProtection:
        displayProtection = "N/A"
    else:
        displayProtection = displayProtection.text

    return displaySpecs, maxRefreshRate, imperialDisplaySize, metricDisplaySizeSquared, widthPixels, heightPixels, displayRatio, displayDensity, displayProtection