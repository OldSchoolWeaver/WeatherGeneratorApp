
#!/usr/bin/env python3
# coding: utf-8


import pandas as pd
import numpy as np
import datetime as dt
import pytest
from Aux import load_csvFile

#Loads weatherforecast_simulation.csv into a data frame
df_simulation= load_csvFile(file_location = 'Simulations/', 
                            file_name = 'weatherforecast_simulation.csv',
                            sep = '|',
                            encoding='utf-8'
                            )

#Loads Locations_HistoricalData.csv into a data frame
df_historical_data= load_csvFile(file_location = 'Data/', 
                            file_name = 'Locations_HistoricalData.csv',
                            sep = '|',
                            encoding='utf-8'
                            )

def test_MinTemperature():
    """
        This test ensures that the minimum temperature value from the simulation is within 
        the range of values from the historical data set. 
    """
    min_temperature_historical_data=df_historical_data['Temperature'].min()
    min_temperature_simulation=df_simulation['Temperature'].min()
    assert min_temperature_simulation >= min_temperature_historical_data 

def test_MaxTemperature():
    """
        This test ensures that the maximum temperature value from the simulation is within 
        the range of values from the historical data set. 
    """
    max_temperature_historical_data=df_historical_data['Temperature'].max()
    max_temperature_simulation=df_simulation['Temperature'].max()
    assert max_temperature_historical_data >= max_temperature_simulation 

def test_MinHumidity():
    """
        This test ensures that the minimum humidity value from the simulation is within 
        the range of values from the historical data set. 
    """
    min_humidity_historical_data=df_historical_data['Humidity'].min()
    min_humidity_simulation=df_simulation['Humidity'].min()
    assert min_humidity_simulation >= min_humidity_historical_data 

def test_MaxHumidity():
    """
        This test ensures that the maximum humidity value from the simulation is within 
        the range of values from the historical data set. 
    """
    max_humidity_historical_data=df_historical_data['Humidity'].max()
    max_humidity_simulation=df_simulation['Humidity'].max()
    assert max_humidity_historical_data >= max_humidity_simulation     

def test_MinPressure():
    """
        This test ensures that the minimum pressure value from the simulation is within 
        the range of values from the historical data set. 
    """
    min_pressure_historical_data=df_historical_data['Pressure'].min()
    min_pressure_simulation=df_simulation['Pressure'].min()
    assert min_pressure_simulation >= min_pressure_historical_data 

def test_MaxPressure():
    """
        This test ensures that the maximum pressure value from the simulation is within 
        the range of values from the historical data set. 
    """
    max_pressure_historical_data=df_historical_data['Pressure'].max()
    max_pressure_simulation=df_simulation['Pressure'].max()
    assert max_pressure_historical_data >= max_pressure_simulation  