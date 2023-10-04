import argparse
from src.get_data import get_data
from sklearn.model_selection import train_test_split
import pandas as pd

def split_data(config_path):
    _,config=get_data(config_path)

    test_size = config["data_split"]["t_size"]
    train_path = config["data_split"]["train"]
    test_path = config["data_split"]["test"]
    rs = config["base"]["random_state"]
    df_path = config["data_processed"]

    df = pd.read_csv(df_path)

    train,test = train_test_split(df, random_state=rs, test_size=test_size)
    train.to_csv(train_path,sep=',',index=False)
    test.to_csv(test_path,sep=',',index=False)

if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parser=args.parse_args()
    split_data(parser.config)