import json
import yaml
import os
import pytest

@pytest.fixture
def config(config_path="params.yaml"):
    with open(config_path) as yaml_file:
        config1=yaml.safe_load(yaml_file)
    return config1

@pytest.fixture
def schema_data(schema_path=os.path.join("test","min_max_schema.json")):
    with open(schema_path) as json_file:
        schema=json.load(json_file)
    return schema