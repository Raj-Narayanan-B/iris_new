import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    "incorrect_values": {
        "SepalLengthCm": 10,
        "SepalWidthCm": 100,
        "PetalLengthCm": 50,
        "PetalWidthCm": 10
    },

    "correct_values": {
        "SepalLengthCm": 5,
        "SepalWidthCm": 3,
        "PetalLengthCm": 3,
        "PetalWidthCm": 1
    },

    "incorrect_cols": {
        "SepalLengthCm ": 10,
        "SepalWidthCm": 100,
        "PetalLengthCm": 50,
        "PetalWidthCm": 10
    }
}

target = {
    "min": 1,
    "max": 3
}


def test_formdata_correct_values(input_data=input_data["correct_values"]):
    response = form_response(input_data)
    assert (target['min'] <= response <= target['max'])  # type: ignore

def test_apidata_correct_values(input_data=input_data['correct_values']):
    response = api_response(input_data)
    assert (target['min'] <= response['prediction'] <= target['max'])  # type: ignore

def test_formdata_incorrect_values(input_data=input_data["incorrect_values"]):
    with pytest.raises(prediction_service.prediction.Not_in_range): # type: ignore
        res = form_response(input_data)

def test_apidata_incorrect_values(input_data=input_data["incorrect_values"]):
    response = api_response(input_data)
    assert response['response'] == prediction_service.prediction.Not_in_range().message # type: ignore

def test_apidata_incorrect_cols(input_data=input_data["incorrect_cols"]):
    response=api_response(input_data)
    assert response["response"] == prediction_service.prediction.Not_in_cols().message # type: ignore

def test_config(config):
    assert 42 == config["base"]['random_state']

def test_schema(schema_data):
    assert 4.3==schema_data["SepalLengthCm"]["min"]