import os
import sys
from email import header

from src.exception import CustomException
from src.logger import logger
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from src.components import DataTransformation,ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path:str =os.path.join('artifacts','train.csv')
    test_data_path:str =os.path.join('artifacts','test.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()


    def initiate_data_ingestion(self):
        logger.info("Initiating data ingestion")
        try:
            df = pd.read_csv("notebook/data/stud.csv")
            logger.info("Read the data as a dataframe")
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            logger.info("Train and Test split initiated")
            train_data,test_data = train_test_split(df,test_size=0.2,random_state=42)

            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            return self.ingestion_config.train_data_path,self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    obj2 = DataTransformation()
    obj3 = ModelTrainer()
    train_path, test_path = obj.initiate_data_ingestion()
    train_arr, test_arr = obj2.apply_preprocessor(train_path, test_path)
    print(obj3.initiate_model_trainer(train_arr,test_arr))







