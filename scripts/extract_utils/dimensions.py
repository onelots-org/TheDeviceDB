import bs4
import pint
import re

ureg = pint.UnitRegistry()

def manipulate_dimensions(dimensions):
    result = {}
    parts = re.split(r'(Unfolded|Folded):', dimensions)

    if len(parts) == 1:
        nums = re.findall(r'[\d.]+', dimensions.split("mm")[0])
        return [float(n) for n in nums]

    i = 1
    while i < len(parts) - 1:
        label = parts[i].strip()
        values = parts[i + 1].strip()
        nums = re.findall(r'[\d.]+', values.split("mm")[0])
        result[label] = [float(n) for n in nums]
        i += 2

    return result

def convert_dimensions(metricDimensions):
    if isinstance(metricDimensions, dict):
        return {
            label: {
                "Metric (mm)": metricDimensions[label],
                "Imperial (in)": [round(ureg(f"{n} mm").to("in").magnitude, 2) for n in metricDimensions[label]]
            }
            for label in metricDimensions
        }
    else:
        return {
            "Metric (mm)": metricDimensions,
            "Imperial (in)": [round(ureg(f"{n} mm").to("in").magnitude, 2) for n in metricDimensions]
        }

def extract_dimensions(page):
    prettyresult = bs4.BeautifulSoup(page.text, "html.parser")

    rawDimensions = prettyresult.select_one("[data-spec='dimensions']").text
    metricDimensions = manipulate_dimensions(rawDimensions)
    dimensions = convert_dimensions(metricDimensions)

    weight = prettyresult.select_one("[data-spec='weight']").text
    sims = prettyresult.select_one("[data-spec='sim']").text

    metricWeight, imperialWeight = weight.split("g")[0].strip(), weight.split("(")[1].replace(" lb)", "").replace(" oz)", "")

    if "No" in sims:
        sims = "N/A"
    else:
        sims = [sim.strip().replace(" ", "") for sim in sims.split("+")]

    return dimensions, metricWeight, imperialWeight, sims
