#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import random
from Aux import load_csvFile
import sys

class WeatherSimulation():
    '''
    Initialise state for an instance of a weather simulation.
    '''
    def __init__(self):
            self.df_historical_data = load_csvFile('Data/', 
                                                   'Locations_HistoricalData.csv', 
                                                    encoding = 'UTF-8', 
                                                    sep = '|'
                                                   )
    
    def generate(self, random_date):
        
        """
        This function receives a data frame with the weather historical data 
        and random data. It uses an algorithm to do a Linear Interpolation (formula below) to 
        predict the weather values for that random date. The idea of this simulation is to create 
        values for that specific random date within the intervals of the values of the historical 
        data data set.
        The function returns a data frame with the weather forecast for that specific date for each
        location.
        Linear Interpolation Formula:  y= y0 + (y1-y0)*((x-x0)/(x1-x0))
        https://en.wikipedia.org/wiki/Linear_interpolation
                
        Returns:
        df_simulation : pandas data frame with the forecast of the data for each location 
        
        """

        random_date=random_date
        month = random_date.month
        df_historical_data = self.df_historical_data
        
        aux = 0
        # The available data set only contains values from 2014 to 2018
        x = round(random.uniform(2014, 2018),2)
        x0 = int(x)
        x1 = int(x) + 1
        
        
        bool_month_year_x0 = (df_historical_data['Year'] == x0) & (df_historical_data['Month'] == month) 
        bool_month_year_x1 = (df_historical_data['Year'] == x1) & (df_historical_data['Month'] == month)
        
        df_historical_data_x0 = df_historical_data[bool_month_year_x0]
        df_historical_data_x1 = df_historical_data[bool_month_year_x1]
        
        
        cols = ['Location','Position','LocalTime','Conditions','Temperature','Pressure','Humidity']
        df_simulation = pd.DataFrame(columns=cols)
        
        list_of_locations = df_historical_data['Location'].unique()
    
        
        for location in list_of_locations:
                      
            city=location.split(',')[0]
    
            position=df_historical_data_x0.loc[df_historical_data_x0['Location']==location,'Position']
            position=position.values[0]
            
            temperature_y0=df_historical_data_x0.loc[df_historical_data_x0['Location']==location,'Temperature']
            temperature_y1=df_historical_data_x1.loc[df_historical_data_x1['Location']==location,'Temperature']
            
            temperature = temperature_y0.values[0] + (temperature_y1.values[0] - temperature_y0.values[0]) * ((x-x0)/(x1-x0))
            
            humidity_y0=df_historical_data_x0.loc[df_historical_data_x0['Location']==location,'Humidity']
            humidity_y1=df_historical_data_x1.loc[df_historical_data_x1['Location']==location,'Humidity']
            
            humidity = humidity_y0.values[0] + (humidity_y1.values[0] - humidity_y0.values[0]) * ((x-x0)/(x1-x0))
            
            pressure_y0=df_historical_data_x0.loc[df_historical_data_x0['Location']==location,'Pressure']
            pressure_y1=df_historical_data_x1.loc[df_historical_data_x1['Location']==location,'Pressure']
            
            pressure = pressure_y0.values[0] + (pressure_y1.values[0] - pressure_y0.values[0]) * ((x-x0)/(x1-x0))
            
            if (humidity > 80) & (temperature > 0):
                condition = 'Rain'
            elif (humidity > 75) & (temperature < 0):
                condition = 'Snow'
            else:
                condition = 'Sunny'
            
            df_simulation = df_simulation.append(
                                                    {'Location': city, 
                                                     'Position': position,
                                                     'LocalTime': random_date.isoformat(),
                                                     'Conditions': condition,
                                                     'Temperature': round(temperature,1),
                                                     'Humidity': int(humidity),
                                                     'Pressure': round(pressure,1)   
                                                    }, ignore_index=True 
                                                )
            
            aux=aux + 1          
        
        return df_simulation 

