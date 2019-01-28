#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import random
import sys

def save_csvFile(df,file_location,file_name,sep,encoding):
    
    """
    This function receives a data frame saves it as csv file. By default 
    all csv files will be saved on the same data folder (WeatherGenerator/Data). 
    
    Args:
        df : Pandas data frame (source data)
        file_location : file source folder
        file_name: file source name
        sep: Delimiter to use
        encoding: Encoding to use for UTF when reading/writing
        
    """
    try:
        date=datetime.datetime.now().replace(microsecond=0)
        fullpath=file_location + file_name
        df.to_csv(fullpath, sep=sep, encoding=encoding, index=False, header=True)
    except IOError:
        print('Error saving the file: ' , file_name)
        sys.exit(1)
    
def load_csvFile(file_location, file_name,sep,encoding):
    
    """
    This function receives a string with the file location and the file name 
    and loads into a data frame
    
    Args:
        file_location : file source folder
        file_name: file source name
        sep: Delimiter to use
        encoding: Encoding to use for UTF when reading/writing   
        
    Returns:
        df : pandas data frame with the data from the file_name
        
    """
    try:
        fullpath=file_location+file_name
        df = pd.read_csv(fullpath, encoding=encoding,sep=sep)
        return df
    except IOError:
        print('Error loading the file: ' , file_name)
        sys.exit(1)

def get_randomDate(start_date, end_date):
    
    """
    This function will return a random datetime between two datetime 
    objects.
    
    Args:
        start_dt : date time object that represents the start date
        end_dt: date time object that represents the end date
        
    Returns:
        random_date : date time object 
        
    """
        
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    
    random_date = start_date + datetime.timedelta(seconds=random_second)

    return random_date

