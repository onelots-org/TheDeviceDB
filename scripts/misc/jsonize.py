import json

def jsonize(deviceName,
               networkTechnologiesList, twoGBands, threeGBands, fourGBands, fiveGBands,
               launchYear,
               metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims,
               displaySpecs, maxRefreshRate, metricDisplaySizeSquared, imperialDisplaySize,
               widthPixels, heightPixels, displayRatio, displayDensity,
               stockOsLaunchName, stockOsLaunchVersion, stockLaunchCustomRom, stockLaunchCustomRomVersion, stockAndroidLaunchCodename, maxAndroidVersionUpdate,
               chipsets
               ):

    page = {
        "Device Name": deviceName,
        "Informations": {
            "Network": {
                "Technologies": networkTechnologiesList,
                "2G Bands": twoGBands,
                "3G Bands": threeGBands,
                "4G Bands": fourGBands,
                "5G Bands": fiveGBands
            },
            "Launch Year": launchYear,
            "Body": {
                "Dimensions": {
                    "Metric (mm)": metricDimensions,
                    "Imperial (in)": imperialDimensions
                },
                "Weight": {
                    "Metric (g)": metricWeight,
                    "Imperial (oz)": imperialWeight
                },
                "Sim": sims
            },
            "Display": {
                "Specifications": displaySpecs,
                "Max Refresh Rate": maxRefreshRate,
                "Size": {
                    "Inches": imperialDisplaySize,
                    "Square centimeters": metricDisplaySizeSquared
                },
                "Resolution": {
                    "Size": {
                        "Width": widthPixels,
                        "Heigth": heightPixels,
                    },
                    "Ratio": displayRatio,
                    "Density": displayDensity
                },
            },
            "Platform Informations": {
                "OS": {
                    "Stock OS Name": stockOsLaunchName,
                    "Stock OS Version": stockOsLaunchVersion,
                    "Stock Android Version Codename": stockAndroidLaunchCodename,
                    "Max Android Version Update": maxAndroidVersionUpdate,
                    "Stock Custom OS": stockLaunchCustomRom,
                    "Stock Custom OS Version": stockLaunchCustomRomVersion
                },
                "CPU": chipsets,
            }
        }
    }
    return page
# "CPU": chipsets because Samsung thought it was a BRILLIANT idea to have 2 SoCs for 1 device.