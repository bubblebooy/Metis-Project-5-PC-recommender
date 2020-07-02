# %load flask_app/recommender.py

import pandas as pd
import numpy as np
from sklearn.metrics import pairwise
from sklearn.preprocessing import StandardScaler

class Recommender:
    def __init__(self, drop_columns = [], distance_metric = pairwise.euclidean_distances, preprocessors = [StandardScaler()],feature_weights = {}):
        self.distance_metric = distance_metric
        self.build_list = None
        self.drop_columns = drop_columns
        self.preprocessors = preprocessors
        if not self.preprocessors:
            self.preprocessors = []
        self.feature_weights = feature_weights
        
        
    def check_is_fitted(self):
        if self.build_list is None:
            raise Exception("""This Recommender instance is not fitted
            yet. Call 'fit' with a build_list as an argument before using this
            estimator.""")
        
    def set_drop_columns(self, drop_columns):
        self.drop_columns = drop_columns
        
    def preprocesses(self, build_list):
        build_list = build_list.drop(columns = self.drop_columns, errors='ignore').dropna()
        build_list_cols = build_list.columns
        for preprocessor in self.preprocessors:
            build_list = preprocessor.transform(build_list)
        for feature in self.feature_weights:
            try:
                build_list = pd.DataFrame(build_list, columns = build_list_cols)
                build_list[feature] = build_list[feature] * self.feature_weights[feature]
            except:
                raise Exception("feature_weights do not work with preprocessors the change the number of features")
            
        return build_list
        #transform standardization 
        #transform dim reduction?
    
    def fit(self, build_list):
        self.build_list = build_list
        
        build_list = build_list.drop(columns = self.drop_columns, errors='ignore').dropna()
        
        for preprocessor in self.preprocessors:            
            build_list = preprocessor.fit_transform(build_list)
#         if self.scaler:
#             self.scaler.fit(build_list.drop(columns = self.drop_columns, errors='ignore').dropna())
        #fit standardization 
        #fit dim reduction?
        
    def recommend(self, input_builds, fixed_columns = {}, return_type = 'index'):
        self.check_is_fitted()
        if isinstance(input_builds , pd.Series):
            input_builds = input_builds.to_frame().T
        elif not isinstance(input_builds , pd.DataFrame):
            raise Exception('input_builds should be a pd.Series or pd.DataFrame')
        build_list = self.build_list
        for col in fixed_columns:
            build_list = build_list[build_list[col] == fixed_columns[col]]
        
        distances = self.distance_metric(X = self.preprocesses(build_list),
                                         Y = self.preprocesses(input_builds))
        distances = distances.sum(axis = 1)
        
        if return_type == 'index':
            return self.build_list.index[distances.argsort()]
        elif return_type == 'distances':
            return distances

        return distances.argsort()
