import yaml
import argparse
import pandas as pd


def read_params(config_path):
    with open(config_path) as yaml_file:
        config=yaml.safe_load(yaml_file)
    return (config)

def get_data(config_path):
    config=read_params(config_path)

    df_path=config["data_source"]["s3_source"]
    df=pd.read_csv(df_path,sep=',')
    # print (df)
    return (df,config)


if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parser=args.parse_args()
    get_data(parser.config)