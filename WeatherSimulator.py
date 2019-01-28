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
        Creates a weather simulation given a random date for specific locations
    '''
    
    def __init__(self):

        '''
        Initialise state for an instance of a weather simulation.
        '''
        self.df_historical_data = load_csvFile('Data/', 
                                                'Locations_HistoricalData.csv', 
                                                encoding = 'UTF-8', 
                                                sep = '|'
                                                )
    
    def generate(self, random_date):
        
        """
        This function generates weather values for 10 sites consistent with their geographical 
        location and the period of the year. It uses an algorithm to do a Linear Interpolation 
        (formula below) to generate "real" weather values, using random numbers, from a limited 
        historical data set.
        A simulation is performed. A specific number is generated from the possible dates of the 
        historical data set. Once this number is generated the function sets the values for all the 
        features in this data set.
        The function returns a data frame with the weather forecast for that specific date for each
        location.
        Linear Interpolation Formula:  y= y0 + (y1-y0)*((x-x0)/(x1-x0))
        https://en.wikipedia.org/wiki/Linear_interpolation

        Where:
                y0 = Feature value for that specific year with the random date month
                y1 = Feature value for that specific year + 1 with the random date month
                x = random float that represents an year of the historical value (ex:2014.45)
                x0 = int that represents the year of x
                x1 = int that represnet the year of x+1          
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
            
            if round(temperature,1) > 0:
                temperature_str = '+' + str(round(temperature,1))
            else:
                temperature_str = str(round(temperature,1))    

            df_simulation = df_simulation.append(
                                                    {'Location': city, 
                                                     'Position': position,
                                                     'LocalTime': random_date.isoformat(),
                                                     'Conditions': condition,
                                                     'Temperature': temperature_str,
                                                     'Humidity': int(humidity),
                                                     'Pressure': round(pressure,1)   
                                                    }, ignore_index=True 
                                                )
            
            aux=aux + 1          
        
        return df_simulation 

