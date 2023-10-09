import os
import yaml
import joblib
import argparse
import json
import numpy as np

class Not_in_cols(Exception):
    def __init__(self, message="Not in columns"):
        self.message=message
        super().__init__(self.message)

class Not_in_range(Exception):
    def __init__(self, message="Values are not in range"):
        self.message=message
        super().__init__(self.message)

config_path="params.yaml"
schema_path=os.path.join("prediction_service","min_max_schema.json")

def read_args(config_path):
    with open(config_path) as yaml_file:
        config=yaml.safe_load(yaml_file)
    return config

def read_schema(schema_path):
    with open(schema_path) as json_file:
        schema=json.load(json_file)
    return schema

def form_response(dict_data):
    if validate_data(dict_data):
        data=dict_data.values()
        data = [list(map(float,data))]
        prediction=predict(data)
        return prediction
    
def api_response(dict_data):
    schema=read_schema(schema_path)
    try:
        if validate_data(dict_data):
            data=dict_data.values()
            data=np.array([list(data)])
            prediction=predict(data)
            prediction = {"prediction":prediction}
            return prediction
    except Not_in_range as e:
        response = {"The expected range":schema,"response":str(e)}
        return response

    except Not_in_cols as e:
        response = {"The expected columns": list(schema.keys()), "response":str(e)}
        return response

    except Exception as e:
        return {"response":str(e)}
    
def validate_data(dict_data):
    schema=read_schema(schema_path)
    def validate_cols(col):
        if col not in schema.keys():
            raise Not_in_cols
    
    def validate_values(col,val):
        if not (schema[col]['min'] <= float(dict_data[col]) <= schema[col]['max']):
            raise Not_in_range
        
    for col,val in dict_data.items():
        validate_cols(col)
        validate_values(col,val)
    
    return True

def predict(data):
    config=read_args(config_path)
    model_path = os.path.join("prediction_service","model.joblib")
    model=joblib.load(model_path)
    prediction=model.predict(data).tolist()[0]
    try:
        if prediction in [1,2,3]:
            return prediction
        else:
            raise Not_in_range
    except Not_in_range:
        return "Unexpected Result!"
        

# if __name__=="__main__":
#     params_args = argparse.ArgumentParser()
#     params_args.add_argument("--config",default="params.yaml")
#     params_parser=params_args.parse_args()

#     schema_args = argparse.ArgumentParser()
#     schema_args.add_argument("--config",default=os.path.join("prediction_service","min_max_schema.json"))
#     schema_parser=schema_args.parse_args()

#     read_args(params_parser.config,schema_parser.config)