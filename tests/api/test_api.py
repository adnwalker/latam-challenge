import unittest

from fastapi.testclient import TestClient
from challenge import app
from unittest.mock import patch


class TestBatchPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
    def test_should_get_predict(self):
        data = {
                "flights": [
                    {
                        "OPERA": "Grupo LATAM", 
                        "TIPOVUELO": "I", 
                        "MES": 12
                    }
                ]
        }
        # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0])) # change this line to the model of chosing
        with patch("challenge.model.DelayModel.predict") as mock_predict:
            # Set the desired return value for the mock prediction
            mock_predict.return_value = [0]
            response = self.client.post("/predict", json=data["flights"])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"predict": [0]})
    

    def test_should_failed_unkown_column_1(self):
        data = {       
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N",
                    "MES": 13
                }
            ]
        }
        # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))# change this line to the model of chosing
        with patch("challenge.model.DelayModel.predict") as mock_predict:
            mock_predict.return_value = [0]  # Set the desired return value for the mock prediction
            response = self.client.post("/predict", json=data["flights"])
            self.assertEqual(response.status_code, 400)

    def test_should_failed_unkown_column_2(self):
        data = {        
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "O", 
                    "MES": 13
                }
            ]
        }
        # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))# change this line to the model of chosing
        with patch("challenge.model.DelayModel.predict") as mock_predict:
            mock_predict.return_value = [0]  # Set the desired return value for the mock prediction
            response = self.client.post("/predict", json=data["flights"])
            self.assertEqual(response.status_code, 400)
    
    def test_should_failed_unkown_column_3(self):
        data = {        
            "flights": [
                {
                    "OPERA": "Argentinas", 
                    "TIPOVUELO": "O", 
                    "MES": 13
                }
            ]
        }
        # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))
        with patch("challenge.model.DelayModel.predict") as mock_predict:
            mock_predict.return_value = [0]  # Set the desired return value for the mock prediction
            response = self.client.post("/predict", json=data["flights"])
            self.assertEqual(response.status_code, 400)