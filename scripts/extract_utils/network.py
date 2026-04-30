import bs4

def extract_network(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")
    networkTechnologiesList = prettyresult.select_one("[data-spec='nettech']")
    twoGBands = prettyresult.select_one("[data-spec='net2g']")
    threeGBands = prettyresult.select_one("[data-spec='net3g']")
    fourGBands = prettyresult.select_one("[data-spec='net4g']")
    fiveGBands = prettyresult.select_one("[data-spec='net5g']")

    networkTechnologiesList = networkTechnologiesList.text if networkTechnologiesList else "N/A"
    twoGBands = twoGBands.text if twoGBands else "N/A"
    threeGBands = threeGBands.text if threeGBands else "N/A"
    fourGBands = fourGBands.text if fourGBands else "N/A"
    fiveGBands = fiveGBands.text if fiveGBands else "N/A"

    if "No cellular connectivity" not in networkTechnologiesList:
        networkTechnologiesList = [tech.strip().replace(" ", "") for tech in networkTechnologiesList.split("/")]
    if "N/A" not in twoGBands:
        twoGBands = [twog.strip() for twog in twoGBands.split("/")]
    if "N/A" not in threeGBands and threeGBands:
        threeGBands = [threeg.strip() for threeg in threeGBands.split("/")]
    if "N/A" not in fourGBands and fourGBands:
        fourGBands = [fourg.strip() for fourg in fourGBands.split(",")]
    if "N/A" not in fiveGBands:
        fiveGBands = [fiveg.strip() for fiveg in fiveGBands.split(",")]

    return networkTechnologiesList, twoGBands, threeGBands, fourGBands, fiveGBands