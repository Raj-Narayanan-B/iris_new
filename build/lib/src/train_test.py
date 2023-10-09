from src.get_data import read_params
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,log_loss
import joblib
import json
import os

def metrics(y_true,y_pred):
    return(accuracy_score(y_true=y_true,y_pred=y_pred))

def train_test(config_path):
    config=read_params(config_path)
    
    train_df_path=config["data_split"]["train"]
    test_df_path=config["data_split"]["test"]
    target=config["base"]["target_col"]

    report_param_path=config["reports"]["params"]
    report_score_path=config["reports"]["scores"]

    crit=config["estimators"]["DecisionTreeClassifier"]["params"]["criterion"]
    max_depth=config["estimators"]["DecisionTreeClassifier"]["params"]["max_depth"]

    model_path = config["model_dir"]

    train_df=pd.read_csv(train_df_path,sep=",")
    test_df=pd.read_csv(test_df_path,sep=",")

    x_train=train_df.drop(columns=target)
    y_train=train_df[target]

    x_test=test_df.drop(columns=target)
    y_test=test_df[target]

    model=DecisionTreeClassifier(criterion=crit, max_depth=max_depth)
    model.fit(x_train,y_train)
    y_pred = model.predict(x_test)

    # print("y_pred: ",np.unique(y_pred))
    # print("y_test: ",np.unique(y_test))

    accuracy_score=metrics(y_true = y_test, y_pred = y_pred)

    os.makedirs("report",exist_ok=True)

    with open(report_param_path,"w") as file:
        params={
            "criterion": crit,
            "max_depth": max_depth
        }
        json.dump(params,file,indent=4)
    
    with open(report_score_path,"w") as file:
        score={
            "accuracy_score": accuracy_score
        }
        json.dump(score,file,indent=4)
    
    model_path = os.path.join(model_path,"model.joblib")
    joblib.dump(model,model_path)

if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parser=args.parse_args()
    train_test(parser.config)