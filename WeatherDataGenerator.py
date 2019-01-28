#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import datetime as dt
import json
import requests
import forecastio
import datetime
from dateutil.relativedelta import relativedelta
import sys


class WeatherData():
    
    def __init__(self,google_api_key,dark_sky_api_key):
        
        '''
        This __init__ function runs when the class is initiated
        '''
        self.google_api_key=google_api_key
        self.dark_sky_api_key=dark_sky_api_key
    
    def loadLocations(self):
        
        """
        This function loads the location csv file into a data frame. By default 
        the location csv file is on the directory WeatherGenerator/Data. 
    
        Returns:
        df_locations : pandas data frame with the location data
        
        """
    
        df_locations=pd.read_csv('Data/data_locations.csv')
        df_locations.rename(columns={'':'Location'},inplace=True)
        
        return df_locations
        
    def generateGeographicCoordinates(self,df_locations):
        
        """
        This function receives a data frame with all the locations and uses the 
        google api to retrieve the correspondent coordinates for each location
        (latitute and longitude). The function returns a panda data frame with
        the locations and theirs correspondent geographic coordinates
        
        Args:
        df_location : pandas data frame with the location data
        
        Returns:
        df_geographic_coordinates : pandas data frame with the geographic coordinates data 
        
        """
        
        df_geographic_coordinates = df_locations
        df_geographic_coordinates['Latitude'] = np.nan
        df_geographic_coordinates['Longitude'] = np.nan
                
        url_google_geo_coordinates= 'https://maps.googleapis.com/maps/api/geocode/json'
        
        list_of_locations = df_locations['Location'].unique()
        
        for location in list_of_locations:
        
            parameters={'address': location,'key':self.google_api_key}
            
            #Call google geo coordinates api, returns a JSON File
            try:
                request_geo_coordinates=requests.get(url_google_geo_coordinates,params=parameters)
            except requests.exceptions.RequestException as e:  
                print ('Error requesting API call https://maps.googleapis.com/maps/api/geocode/: ' , e)
                sys.exit(1)
            
            json=request_geo_coordinates.json()
              
            latitude=json['results'][0]['geometry']['location']['lat']
            longitude=json['results'][0]['geometry']['location']['lng']
        
            df_geographic_coordinates.loc[df_geographic_coordinates['Location']==location,'Longitude'] = longitude
            df_geographic_coordinates.loc[df_geographic_coordinates['Location']==location,'Latitude'] = latitude
        
        return df_geographic_coordinates

    def generateGeographicElevation(self,df_geographic_coordinates):
        
        """
        This function receives a data frame with all the locations and coordinates 
        and uses a google api to retrieve the correspondent elevation for each location.
        The function returns a panda data frame with locations, geographic coordinates
        and elevation.
        
        Args:
        df_GeographicCoordinates : pandas data frame with the location and geographic coordinates data
        
        Returns:
        df_geographic_coordinates : pandas data frame with the location, geographic coordinates 
                                    and elevation data 
        
        """

        
        df_geographic_coordinates_altitude = df_geographic_coordinates
        df_geographic_coordinates_altitude['Elevation'] = np.nan
        aux=0
        
        url_google_geo_elevation= 'https://maps.googleapis.com/maps/api/elevation/json'
        
        list_of_locations = df_geographic_coordinates['Location'].unique()
        
        for location in list_of_locations:
                      
            latitude=df_geographic_coordinates.loc[df_geographic_coordinates['Location']==location,'Latitude']
            longitude=df_geographic_coordinates.loc[df_geographic_coordinates['Location']==location,'Longitude']
            
            parameters={'locations': str(latitude[aux]) + ',' + str(longitude[aux]),'key':self.google_api_key}
            
            #Call google geo elevation api, returns a JSON File
            try:
                request_geo_elevation=requests.get(url_google_geo_elevation,params=parameters)
            except requests.exceptions.RequestException as e:  
                print ('Error requesting API call https://maps.googleapis.com/maps/api/elevation/: ' , e)
                sys.exit(1)
            
            json=request_geo_elevation.json()
            elevation=json['results'][0]['elevation']
            
            df_geographic_coordinates_altitude.loc[df_geographic_coordinates_altitude['Location']==location,'Elevation'] = round(elevation,2)
            
            aux=aux+1
            
        return df_geographic_coordinates_altitude
    
    
    def generateHistoricalData(self,df_geographic_coordinates_altitude):
        
        """
        This function receives a data frame with all the locations and coordinates 
        and uses the darksky api to retrieve the weather historical data for each location.
        The function returns a panda data frame with the historical data for temperature, 
        pressure and humidity for each location.
        
        Args:
        df_geographic_coordinates_altitude : pandas data frame with the location and geographic coordinates 
                                             and elevation data
        
        Returns:
        df_historical_data : pandas data frame with weather historical data for each location 
        
        """
        dark_sky_api_key = self.dark_sky_api_key
        url_darksky='https://api.darksky.net/forecast/'
        
        start_date = datetime.datetime.strptime("2014-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime("2014-02-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        
         
        cols = ['Location','Position','Year','Month','LocalTime','Conditions','Temperature','Pressure','Humidity']
        df_historical_data = pd.DataFrame(columns=cols)
        
        list_of_locations = df_geographic_coordinates_altitude['Location'].unique()
        
        
        while (start_date <= end_date):
            
            aux =0
            
            for location in list_of_locations:
        
                latitude=df_geographic_coordinates_altitude.loc[df_geographic_coordinates_altitude['Location']==location,'Latitude']
                longitude=df_geographic_coordinates_altitude.loc[df_geographic_coordinates_altitude['Location']==location,'Longitude']
                elevation=df_geographic_coordinates_altitude.loc[df_geographic_coordinates_altitude['Location']==location,'Elevation']
                position=str(latitude[aux]) + ',' + str(longitude[aux]) + ',' + str(elevation[aux])
                
                
                
                #Call forescastio api, returns a JSON File
                try:
                    forecast = forecastio.load_forecast(dark_sky_api_key, 
                                                        str(latitude[aux]), 
                                                        str(longitude[aux]),
                                                        time=start_date, 
                                                        units='si')
                
                except requests.exceptions.RequestException as e:  
                    print ('Error requesting API call https://api.darksky.net/forecast/: ' , e)
                    sys.exit(1)
                
                
                h = forecast.daily()
                d = h.data
                
                
                for p in d:
                     
                    temp_high = p.d.get("temperatureHigh", 0)
                    temp_low = p.d.get("temperatureLow", 0)
                    temp = round((temp_high + temp_low) / 2,1)
                    humidity = round(p.d.get("humidity", 0),1)
                    pressure = round(p.d.get("pressure", 0),1)
                    
                    
                    if (humidity > 0.80) & (temp > 0):
                        condition = 'Rain'
                    elif (humidity > 0.75) & (temp < 0):
                        condition = 'Snow'
                    else:
                        condition = 'Sunny'

                df_historical_data = df_historical_data.append(
                                                                {'Location': location, 
                                                                 'Position': position,
                                                                 'Year': start_date.year,
                                                                 'Month': start_date.month,
                                                                 'LocalTime': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                                                                 'Conditions': condition,
                                                                 'Temperature': temp,
                                                                 'Humidity': int(humidity * 100),
                                                                 'Pressure': pressure   
                                                                }, ignore_index=True 
                                                            )
                aux=aux+1

            start_date = start_date + relativedelta(months=+1) 
                
        return df_historical_data
    