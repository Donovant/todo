fall = ['10']  # October
summer = ['07']  # July
spring = ['05']  # May
winter = ['02']  # February
biannually = ['06', '12']  # June and December
quarterly = ['03', '06', '09', '12']  # March, June, September, December
monthly = ['01', '02', '03', '04', '05', '06',
           '07', '08', '09', '10', '11', '12']
years = ['2019', '2020', '2021', '2022', '2023', '2024', 
         '2025', '2026', '2027', '2028', '2029', '2030']

tasks = {
    -2: {
        "dom": ['01'],
        "month": monthly,
        "year": years,
        "name": "Test Task!!"
    },
    1: {
        "dom": ['10'],
        "month": monthly,
        "year": years,
        "name": "Replace HVAC Filter"
    },
    2: {
        "dom": ['12'],
        "month": monthly,
        "year": years,
        "name": "Clean Garbage Disposal"
    },
    3: {
        "dom": ['12'],
        "month": monthly,
        "year": years,
        "name": "Clean Hood Filters"
    },
    4: {
        "dom": ['15'],
        "month": monthly,
        "year": years,
        "name": "Check Sump Pump/Radon Mitigation System"
    },
    5: {
        "dom": ['99'],
        "month": monthly,
        "year": years,
        "name": "none/available"
    },
    6: {
        "dom": ['20'],
        "month": quarterly,
        "year": years,
        "name": "Test Smoke/Carbon Monoxide Detectors"
    },
    7: {
        "dom": ['20'],
        "month": quarterly,
        "year": years,
        "name": "Test Garage Door Auto-Reverse And Sensors"
    },
    8: {
        "dom": ['25'],
        "month": quarterly,
        "year": years,
        "name": "Flip Mattresses"
    },
    9: {
        "dom": ['25'],
        "month": quarterly,
        "year": years,
        "name": "Clean Faucet Aerators/Shower Heads"
    },
    10: {
        "dom": ['30'],
        "month": quarterly,
        "year": years,
        "name": "Clean Heat Registers/Vents"
    },
    11: {
        "dom": ['07'],
        "month": biannually,
        "year": years,
        "name": "Replace batteries in smoke/carbon dioxide detectors"
    },
    12: {
        "dom": ['07'],
        "month": biannually,
        "year": years,
        "name": "Replace batteries freezer thermometers"
    },
    13: {
        "dom": ['07'],
        "month": biannually,
        "year": years,
        "name": "Clean Refrigerator/Freezer Coils"
    },
    14: {
        "dom": ['07'],
        "month": summer,
        "year": years,
        "name": "Check/Clean Dryer Vent"
    },
    15: {
        "dom": ['07'],
        "month": biannually,
        "year": years,
        "name": "Clean Windows"
    },
    16: {
        "dom": ['07'],
        "month": biannually,
        "year": years,
        "name": "Check Attic For Leaks"
    },
    17: {
        "dom": ['07'],
        "month": biannually,
        "year": years,
        "name": "Check Washing Machine Hoses"
    },
    18: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Turn On Sprinkler System"
    },
    19: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Check/Re-Adjust Sprinkler Heads"
    },
    20: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Spray Bug Perimeter"
    },
    21: {
        "dom": ['09'],
        "month": fall,
        "year": years,
        "name": "Aerate Lawn"
    },
    22: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Inspect AC"
    },
    23: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Reverse Ceiling Fans"
    },
    24: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Check Window/Door Screens"
    },
    25: {
        "dom": ['09'],
        "month": spring,
        "year": years,
        "name": "Pressure Wash Exterior Of House"
    },
    26: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Turn Off/Flush Sprinkler System"
    },
    27: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Clean Gutters"
    },
    28: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Inspect Fireplace"
    },
    29: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Reverse Ceiling Fans"
    },
    30: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Inspect Roof"
    },
    31: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Check Weather Stripping On Doors"
    },
    32: {
        "dom": ['04'],
        "month": fall,
        "year": years,
        "name": "Inspect Outdoor Lighting"
    },
    33: {
        "dom": ['03'],
        "month": winter,
        "year": years,
        "name": "Check Electrical Outlets"
    },
    34: {
        "dom": ['03'],
        "month": winter,
        "year": years,
        "name": "Flush Water Heater"
    },
    35: {
        "dom": ['05'],
        "month": biannually,
        "year": years,
        "name": "Deep Clean Granite Counters"
    },
    36: {
        "dom": ['11'],
        "month": biannually,
        "year": years,
        "name": "Clean Garage"
    },
    37: {
        "dom": ['13'],
        "month": biannually,
        "year": years,
        "name": "Inspect/Touch-up Paint"
    },
    38: {
        "dom": ['13'],
        "month": quarterly,
        "year": years,
        "name": "Leach Plants"
    },
    39: {
        "dom": ['18'],
        "month": biannually,
        "year": years,
        "name": "Dust Blinds"
    },
    40: {
        "dom": ['18'],
        "month": quarterly,
        "year": years,
        "name": "Clean Ceiling Fans"
    },
    41: {
        "dom": ['02'],
        "month": quarterly,
        "year": years,
        "name": "Clean Inside Of Computers"
    },
    42: {
        "dom": ['02'],
        "month": biannually,
        "year": years,
        "name": "Clean Behind Stove"
    },
    43: {
        "dom": ['02'],
        "month": biannually,
        "year": years,
        "name": "Clean Behind Refrigerator"
    },
    9999: {
        "dom": ['01'],
        "month": ['01'],
        "year": ['2030'],
        "name": "Increment Years In Code"
    }
}
