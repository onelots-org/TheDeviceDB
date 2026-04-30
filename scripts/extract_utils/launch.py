import bs4

def extract_network(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")
    deviceName = prettyresult.find("h1").text
    launchYear = prettyresult.select_one("[data-spec='year']").text.split(",")[0].strip()

    return deviceName, launchYear