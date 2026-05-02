# TheDeviceDB

Aims to create the biggest and most accurate database about android devices.

Contains data for developers such as:
- SoCs informations
- Devices codenames

More to come

TODO :
 
- Scrap devices
- Scrap devices images
- Associate devices with codenames
- Scrap SoCs
- Associate SoCs with devices

## What a device looks like right now :
```json
{
   "Device Name":"Samsung Galaxy Tab S7 FE",
   "Informations":{
      "Network":{
         "Technologies":[
            "GSM",
            "HSPA",
            "LTE",
            "5G"
         ],
         "2G Bands":[
            "GSM 850",
            "900",
            "1800",
            "1900"
         ],
         "3G Bands":[
            "HSDPA 850",
            "900",
            "1700(AWS)",
            "1900",
            "2100"
         ],
         "4G Bands":[
            "1",
            "2",
            "3",
            "4",
            "5",
            "7",
            "8",
            "12",
            "13",
            "17",
            "20",
            "25",
            "26",
            "28",
            "32",
            "38",
            "40",
            "41",
            "66"
         ],
         "5G Bands":[
            "1",
            "3",
            "5",
            "7",
            "8",
            "20",
            "28",
            "38",
            "40",
            "41",
            "77",
            "78 SA/NSA/Sub6"
         ]
      },
      "Launch Year":"2021",
      "Body":{
         "Dimensions":{
            "Metric (mm)":[
               284.8,
               185.0,
               6.3
            ],
            "Imperial (in)":[
               11.21,
               7.28,
               0.25
            ]
         },
         "Weight":{
            "Metric (g)":"608",
            "Imperial (oz)":"1.34"
         },
         "Sim":[
            "Nano-SIM(cellularmodelonly)"
         ]
      },
      "Display":{
         "Specifications":[
            "TFT LCD"
         ],
         "Max Refresh Rate":"None",
         "Size":{
            "Inches":"12.4",
            "Square centimeters":"445.8"
         },
         "Resolution":{
            "Size":{
               "Width":"1600",
               "Heigth":"2560"
            },
            "Ratio":"16:10",
            "Density":"243"
         }
      },
      "Platform Informations":{
         "OS":{
            "Stock OS Name":"Android",
            "Stock OS Version":"11",
            "Stock Android Version Codename":"Red Velvet Cake",
            "Max Android Version Update":"14",
            "Stock Custom OS":"One UI",
            "Stock Custom OS Version":"6"
         },
         "CPU":[
            {
               "Vendor":"Qualcomm",
               "Platform":"SM7225",
               "Platform Codename":{
                  "HLOS":"Lito",
                  "Die":[
                     "Bitra",
                     "Lagoon"
                  ]
               },
               "Market Name":"Snapdragon 750G 5G",
               "Processor Engraving Fineness":"8"
            },
            {
               "Vendor":"Qualcomm",
               "Platform":"SM7325",
               "Platform Codename":{
                  "HLOS":"Lahaina",
                  "Die":[
                     "Kodiak",
                     "Yupik"
                  ]
               },
               "Market Name":"Snapdragon 778G 5G",
               "Processor Engraving Fineness":"6"
            }
         ]
      }
   }
}
```