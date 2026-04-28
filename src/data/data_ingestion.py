import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
import yaml
import logging
from src.logger import configure_logger


def load_params(params_path:str) -> dict:
    try:
        with open(params_path,'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retrieved from %s',params_path)
        return params
    
    except FileNotFoundError:
        logging.error('File not found: %s',params_path)
        raise
    except yaml.YAMLError as e:
        logging.error('YAML error: %s',e)
        raise
    except Exception  as e:
        logging.error('Unexpected error: %s',e)
        raise

def load_data(data_url:str)->pd.DataFrame:
    try:
        df = pd.read_csv(data_url)
        logging.info('Data loaded from %s',data_url)
        return df
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the csv file: %s',e)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the data: %s',e)
        raise

def preprocess_data(df:pd.DataFrame) -> pd.DataFrame:
    try:
        logging.info('Preprocessing...')
        final_df = df[df['sentiment'].isin(['positive','negative'])]
        final_df['sentiment'] = final_df['sentiment'].replace({'positive':1,'negative':0})
        logging.info('Data proprecesssing completed')
        return final_df
    
    except KeyError as e:
        logging.error('Missing column in the dataframe:%s',e)
        raise
    except Exception as e:
        logging.error('Unexpected error during preprocessing:%s',e)
        raise

def save_data(train_data:pd.DataFrame,test_data:pd.DataFrame,data_path:str)->None:
    try:
        raw_data_path = os.path.join(data_path,'raw')
        os.makedirs(raw_data_path,exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path,'train.csv'),index=False)
        test_data.to_csv(os.path.join(raw_data_path,'test.csv'),index=False)
        logging.debug('Train and Test data saved to %s',raw_data_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s',e)
        raise

def main():
    test_size = 0.2
    df = load_data(data_url=)