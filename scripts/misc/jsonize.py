import json

def jsonize(deviceName,
               networkTechnologiesList, twoGBands, threeGBands, fourGBands, fiveGBands,
               launchYear,
               metricDimensions, imperialDimensions, metricWeight, imperialWeight, sims,
               displaySpecs, maxRefreshRate, metricDisplaySizeSquared, imperialDisplaySize,
               widthPixels, heightPixels, displayRatio, displayDensity,
               stockAndroidLaunchVersion, stockAndroidLaunchVersionCodename, stockLaunchRom, stockLaunchRomVersion,
               chipsetVendor, chipsetCode, chipsetCodename, chipsetMarketName, chipsetEngravingFineness
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
                    "Android Version": stockAndroidLaunchVersion,
                    "Android Version Codename": stockAndroidLaunchVersionCodename,
                    "Stock OS": stockLaunchRom,
                    "Stock OS Version": stockLaunchRomVersion
                },
                "CPU": {
                    "Vendor": chipsetVendor,
                    "Platform": chipsetCode,
                    "Platform Codename": chipsetCodename,
                    "Market Name": chipsetMarketName,
                    "Processor Engraving Fineness": chipsetEngravingFineness
                }
            }
        }
    }
    return page