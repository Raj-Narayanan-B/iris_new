import argparse
from src.get_data import get_data

def load_data(config_path):
    df,config = get_data(config_path)
    processed_df_path = config["data_processed"]

    df.drop(["Id"],axis=1,inplace=True)
    df["Species"]=df["Species"].map({"Iris-setosa":1, "Iris-versicolor":2, "Iris-virginica":3})
    
    df.to_csv(processed_df_path,sep=',',index=False)
    
if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parser=args.parse_args()
    load_data(parser.config)