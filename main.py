from influxdb import InfluxDBClient
import requests
import json
import pprint
import os

host = os.getenv("INFLUXDB_HOST")
port = os.getenv("INFLUXDB_PORT")
username = os.getenv("INFLUXDB_USER")
password = os.getenv("INFLUXDB_PASS")
client = InfluxDBClient(host, port, username, password)
client.switch_database('sauguspilietis')

print (client.get_list_database())
print (client.get_list_measurements())
res = requests.get('https://api.waqi.info/search/?token=a9dbba418cc7a3cc01000b9afcd69a5f12db7ffd&keyword=lithuania')

all_data = json.loads(res.content)

station_id = {}

data_for_database = []

for station in all_data['data']:
    airQuality = requests.get('https://api.waqi.info/feed/@'+str(station['uid'])+'/?token=a9dbba418cc7a3cc01000b9afcd69a5f12db7ffd')
    airContext = json.loads(airQuality.content)

    if 'w' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['w'] = 0
    if 'o3' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['o3'] = 0
    if 'p' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['p'] = 0
    if 'pm10' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['pm10'] = 0
    if 'wg' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['wg']  = 0
    if 'dev' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['dev'] = 0
    if 'so2' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['so2'] = 0
    if 'pm25' not in airContext['data']['iaqi'].keys():
        airContext['data']['iaqi']['pm25'] = 0

    values = {}
    for k in airContext['data']['iaqi'].keys():
        if airContext['data']['iaqi'][k] == 0:
            values[k] = 0.0
        else:
            values[k] = float(airContext['data']['iaqi'][k]['v'])

    station_id[str(station['uid'])] = [
        station['station']['name'],
        station['station']['geo'],
        station['station']['url'],
        airContext['data']['iaqi']['so2'],
        airContext['data']['iaqi']['o3'],
        airContext['data']['iaqi']['p'],
        airContext['data']['iaqi']['pm10'],
        airContext['data']['iaqi']['wg'],
        airContext['data']['iaqi']['dev'],
        airContext['data']['iaqi']['pm25']
    ]

    data_for_database.append({
        "measurement": "airQuality",
        "tags": {
            "id": station['uid'],
            "name": station['station']['name'],
            "url": station['station']['url'],
            "location": " ".join([str(i) for i in station['station']['geo']])
        },
        "fields": values
    })

print(data_for_database)
client.write_points(data_for_database)


