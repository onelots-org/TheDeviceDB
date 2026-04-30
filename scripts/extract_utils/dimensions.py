import bs4

def extract_network(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")

    dimensions = prettyresult.select_one("[data-spec='dimensions']").text
    weight = prettyresult.select_one("[data-spec='weight']").text
    sims = prettyresult.select_one("[data-spec='sim']").text

    # Manipulate dimensions
    metricDimensions, imperialDimensions = dimensions.split("mm")[0].strip(), dimensions.split("(")[1]
    metricDimensions = [float(metric.strip().replace(" ", "").replace("mm", "")) for metric in
                        metricDimensions.split("x")]
    imperialDimensions = [float(imperial.strip().replace(" ", "").replace("in)", "")) for imperial in
                          imperialDimensions.split("x")]
    # Manipulate weight
    metricWeight, imperialWeight = weight.split("g")[0].strip(), weight.split("(")[1].replace(" lb)", "").replace(
        " oz)", "")
    # Sim : Yes or N/A
    if "No" in sims:
        sims = "N/A"
    else:
        sims = [sim.strip().replace(" ", "") for sim in sims.split("+")]

    return metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims