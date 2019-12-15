# /Users/gchomatas/anaconda3/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import requests
import pandas as pd

def getApacheDrillQuery(sqlQuery):
    return {"queryType" : "SQL", "query" : sqlQuery}

def apacheDrillQueryToDataFrame(sqlQuery, valueColumn, valueType):

    apacheDrillQuery = getApacheDrillQuery(sqlQuery)

    responseAsJson = getQueryResponseAsJson(apacheDrillQuery)

    rows = responseAsJson.get('rows')

    dataFrame = pd.DataFrame.from_dict(rows).astype({valueColumn: valueType, 'timestamp': 'int64'})

    dataFrame.timestamp = pd.to_datetime(dataFrame.timestamp, unit='s')

    return dataFrame

def allSensorMeasurementsToDataFrame():
    sqlQuery = 'select tbl.`timestamp`, tbl.sensor.temperature_humidity_sensor as temperature, tbl.sensor.humidity as humidity, tbl.sensor.pressure as pressure from `dfs`.`/Users/gchomatas/AWS_S3/sensors/senseHAT/parquet` as tbl order by tbl.`timestamp`';

    apacheDrillQuery = getApacheDrillQuery(sqlQuery)

    responseAsJson = getQueryResponseAsJson(apacheDrillQuery)

    rows = responseAsJson.get('rows')

    dataFrame = pd.DataFrame.from_dict(rows).astype({'timestamp': 'int64', 'temperature': 'float64', 'humidity': 'float64', 'pressure': 'float64'})

    dataFrame.timestamp = pd.to_datetime(dataFrame.timestamp, unit='s')

    return dataFrame

def getQueryResponseAsJson(apacheDrillQuery):
    apacheDrillQueryUrl = 'http://localhost:8047/query.json'

    response = requests.post('http://localhost:8047/query.json', json=apacheDrillQuery);

    return response.json()

def createTempratureChart():
    sqlQuery = 'select tbl.`timestamp`, tbl.sensor.temperature_humidity_sensor as temperature from `dfs`.`/Users/gchomatas/AWS_S3/sensors/senseHAT/parquet` as tbl order by tbl.`timestamp`';

    dataFrame = apacheDrillQueryToDataFrame(sqlQuery, 'temperature', 'float64')

    chart = dataFrame.plot(x='timestamp', y='temperature', use_index=True, subplots=True)

def createHumidityChart():
    sqlQuery = 'select tbl.`timestamp`, tbl.sensor.humidity as humidity from `dfs`.`/Users/gchomatas/AWS_S3/sensors/senseHAT/parquet` as tbl order by tbl.`timestamp`';

    dataFrame = apacheDrillQueryToDataFrame(sqlQuery, 'humidity', 'float64')

    chart = dataFrame.plot(x='timestamp', y='humidity', use_index=True, subplots=True)

def createPressureChart():
    sqlQuery = 'select tbl.`timestamp`, tbl.sensor.pressure as pressure from `dfs`.`/Users/gchomatas/AWS_S3/sensors/senseHAT/parquet` as tbl order by tbl.`timestamp`';

    dataFrame = apacheDrillQueryToDataFrame(sqlQuery, 'pressure', 'float64')

    chart = dataFrame.plot(x='timestamp', y='pressure', use_index=True, subplots=True)

def plotAllSensorsWithSubplots():
    allSensorMeasurements = allSensorMeasurementsToDataFrame()

    allSensorMeasurements.pressure = allSensorMeasurements.pressure[allSensorMeasurements.pressure.between(allSensorMeasurements.pressure.quantile(.001), allSensorMeasurements.pressure.quantile(1))]
    
    allSensorMeasurements.plot(x='timestamp', y=['temperature', 'humidity', 'pressure'], use_index=True, subplots=True)
    # allSensorMeasurements.plot(x='timestamp', y=['temperature', 'humidity', 'pressure'], use_index=True, subplots=True, style='k.')
    
    plt.show()

def boxPlotAllSensors():
    allSensorMeasurements.boxplot('temperature')
    allSensorMeasurements.boxplot('humidity')
    allSensorMeasurements.boxplot('pressure')
    plt.show()

def main():
    plotAllSensorsWithSubplots()
    # createTempratureChart()
    # createHumidityChart()
    # createPressureChart()


if __name__ == "__main__":
    main()

