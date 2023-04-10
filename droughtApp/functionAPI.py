import json
import requests
from datetime import datetime, timedelta


def api_results(date):
    api_url = "https://api.aerisapi.com/conditions/summary?client_id=22jRBqhgG631jx2a4x7Io&client_secret=luddtwCbijC5wy6Y1W3IkuFnzqLqQlprinobETxW&for={0}&filter=day&p=70809&fields=periods.temp.minF,periods.temp.maxF,periods.humidity.max,periods.humidity.min,periods.windSpeed.avgMPH,periods.precip.totalIN,periods.solrad.avgWM2".format(date)
    response = requests.get(api_url)
    # print("API output all------------")
    # print(response.json())

    json_data_all = response.json() if response and response.status_code == 200 else None
    Rainfall = {}
    if json_data_all and 'response' in json_data_all:
        if 'periods' in json_data_all['response'][0]: 
            i = 0
            for eachPeriod in json_data_all['response'][0]['periods']:  
                print("For day : ", date)
                # Rainfall total inches
                rainfall = eachPeriod.get('precip')
                rainfall_totalIN = rainfall['totalIN']
                print("rainfall_totalIN = ", rainfall_totalIN)

                # Max and min temperature Farenheit
                minTempF = eachPeriod.get('temp')["minF"]
                maxTempF = eachPeriod.get('temp')["maxF"]
                print("minTempF = ", minTempF,", ", "maxTempF = ", maxTempF)

                # Max and min humidity
                minHumidity = eachPeriod.get('humidity')["min"]
                maxHumidity = eachPeriod.get('humidity')["max"]
                print("minHumidity = ", minHumidity,", ",  "maxHumidity = ", maxHumidity)

                # Wind speed average MPH
                windSpeedMPH = eachPeriod.get('windSpeed')["avgMPH"]
                print("windSpeedMPH = ", windSpeedMPH)

                # Solar radiation average WM2
                solradWM2 = eachPeriod.get('solrad')["avgWM2"]
                print("solradWM2 = ", solradWM2)
    return [rainfall_totalIN, minTempF, maxTempF, minHumidity, maxHumidity, windSpeedMPH, solradWM2]       