#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import random
import sys
from Aux import *
from WeatherSimulator import *
from WeatherDataGenerator import *


def RunSimulation():
    
    """
    This function will create an instance of a simulation and will save the output as
    as csv file
            
    """

    #Initialise variables
    start_date = datetime.datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    random_date = get_randomDate(start_date,end_date)
    
    weather_simulation = WeatherSimulation()

    #Run and save the simulation
    try:
        df = weather_simulation.generate(random_date)
        save_csvFile(df=df,
                     file_location='Simulations/',
                     file_name='weatherforecast_simulation.csv',
                     sep='|',
                     encoding='utf-8'
                    )
    except:
        print('Error running the weather simulator')


def LoadHistoricalData(google_api_key,dark_sky_api_key):
    
    """
    This function will create an instance of a weather data and retrive the historical data 
    for the specific location save the output as csv file
    as csv file
    """

    #Load historical data

    try:
        weather_historical_data=WeatherData(google_api_key,dark_sky_api_key)
        df_locations=weather_historical_data.loadLocations()
        df_geographic_coordinates=weather_historical_data.generateGeographicCoordinates(df_locations)
        df_geographic_elevation=weather_historical_data.generateGeographicElevation(df_geographic_coordinates)
        df_historical_data=weather_historical_data.generateHistoricalData(df_geographic_elevation)
        save_csvFile(df=df_historical_data,
                     file_location='Data/',
                     file_name='Locations_HistoricalData_TEST.csv',
                     sep='|',
                     encoding='utf-8'
                    )
    except:
        print('Error running the weather data generator')
    

if __name__ == '__main__':
    
    #Run Simulation
    #RunSimulation()
    
    #Load historical data
    google_api_key='AIzaSyAu73Qvrzp0OXJ6ORV33VhWj5WlCEBZJes'
    dark_sky_api_key='66d42558987e734a3726c461f576cd13'
    LoadHistoricalData(google_api_key,dark_sky_api_key)
