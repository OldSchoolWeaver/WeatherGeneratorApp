# WeatherGeneratorApp

## Application:

The weather generator is a python application that retrieves data from bellow APIs: 

     • https://maps.googleapis.com/maps/api/elevation/json
     • https://maps.googleapis.com/maps/api/geocode/json
     • https://api.darksky.net/forecast/'

The google APIs provide the data for the coordinates and also for the elevation of each of the 
locations that are described in Locations.csv (Data folder). The Darksky API provides the historical 
weather data for the correspondent locations.

There are five python scripts in this application:

      WeatherDataGenerator - Script responsible to create the historical data set combining the data 
                             from the 3 APIs mentioned above.This script will create a csv output 
                             called Locations_HistoricalData.csv in the Data folder.

      WeatherSimulator - Script responsible to predict the weather forecast given a random date. 
                         It uses a Liner Interpolation formula to create a set of values based on 
                         the historical dataset. This script will create a csv output called 
                         weatherforecast_simulation.csv in the Simulations folder.

      Aux - Script that has re-usable functions that are used across different scripts.                     

      Run - Script that initiates the simulation, or if required generates a new set of historical 
            data. (The darksky API has limit of 1000 calls per day).
            To Initiate the Simulation run the Run.py script 

      UnitTest - Script to initiates 6 unit test on the simulation data set.   

The WeatherGerneratorAPP produces a csv file as an outcome. The csv is described below:

     Location Position Local Time Conditions Temperature Pressure Humidity
     Sydney -33.86,151.21,39 2015-12-23 16:02:12 Rain +12.5 1010.3 97
     Melbourne -37.83,144.98,7 2015-12-25 02:30:55 Snow -5.3 998.4 55
     Adelaide -34.92,138.62,48 2016-01-04 23:05:37 Sunny +39.4 1114.1 12

Where: 

     • Location is an optional label describing one or more positions
     • Position is a comma-separated triple containing latitude, longitude and elevation 
       in metres above sea level
     • Local time is an ISO8601 date time
     • Conditions are either Snow, Rain, Sunny
     • Temperature is in °C
     • Pressure is in hPa
     • Relative humidity is a %

## Dependencies:

The weather generator application requires python3 to be installed and the following packages:

     • numpy==1.16.0
     • pandas==0.24.0
     • python-forecastio==1.4.0
     • requests==2.21.0
     • pytest==4.1.1

## Build:

Git Clone the repository into your local machine. Ensure that Python3 is installed if the above 
dependencies are not installed just execute the following command:

     pip3 install -r requirements.txt

## Run the application

CD into the WeatherGeneratorApp directory and run the the following command:

     python3 Run.py

## Run the Unit Test

CD into the WeatherGeneratorApp directory and run the the following command:

     py.test -v UnitTest.py

