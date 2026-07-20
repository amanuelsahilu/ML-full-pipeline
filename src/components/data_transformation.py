import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logger
import os
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_transformer_object(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            numerical_pipeline = Pipeline([
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])
            categorical_pipeline = Pipeline([
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("onehot_encoder",OneHotEncoder())
            ])
            logger.info(f"Categorical columns: {categorical_columns}")
            logger.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical", numerical_pipeline, numerical_columns),
                    ("categorical", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)


    def apply_preprocessor(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Read train and test data completed")
            logger.info("Obtaining preprocessing object")

            preprocessor = self.get_transformer_object()

            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            feature_train_df = train_df.drop(columns=[target_column_name])
            target_train_df = train_df[target_column_name]
            feature_test_df = test_df.drop(columns=[target_column_name])
            target_test_df = test_df[target_column_name]

            feature_train_arr=preprocessor.fit_transform(feature_train_df)
            feature_test_arr=preprocessor.transform(feature_test_df)

            train_arr = np.c_[feature_train_arr,np.array(target_train_df)]
            test_arr = np.c_[feature_test_arr,np.array(target_test_df)]
            logger.info("Saved preprocessing object.")
            save_object(self.data_transformation_config.preprocessor_file_path,preprocessor)

            return train_arr, test_arr

        except Exception as e:
            raise CustomException(e,sys)



