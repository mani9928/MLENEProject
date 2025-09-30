import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_object
from networksecurity.utils.main_utils.utils import save_numpy_array_data

class DataTransformation:
    def __init__(self,data_valodation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
            try:
                self.data_validation_artifact=data_valodation_artifact
                self.data_transformation_config=data_transformation_config
            except Exception as e:
                raise NetworkSecurityException(e,sys)
    @staticmethod        
    def read_data(self,file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(self)->Pipeline:
        logging.info("Entered the get_data_transformer_object method of Data_Transformation class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized KNN Imputer with params: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            preprocessor: Pipeline = Pipeline([('imputer', imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
            
    def initiate_data_transformation(self)->DataTransformationArtifact:
         logging.info("Entered the initiate_data_transformation method of Data_Transformation class")
         try:
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self,self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self,self.data_validation_artifact.valid_test_file_path)

            #training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            #testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor=self.get_data_transformer_object()
            processor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,processor_object)

            #preparing artifact
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact



         except Exception as e:
              raise NetworkSecurityException(e,sys)