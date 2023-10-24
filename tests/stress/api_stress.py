from locust import HttpUser, task

class StressUser(HttpUser):
    
    @task
    def predict_argentinas(self):
        data = {
            "flights": [
                {
                    "OPERA": "Latin American Wings", 
                    "TIPOVUELO": "I", 
                    "MES": 12
                }
            ]
        }
        self.client.post("/predict", json=data["flights"])

    @task
    def predict_latam(self):
        data = {
            "flights": [
                {
                    "OPERA": "Grupo LATAM", 
                    "TIPOVUELO": "I", 
                    "MES": 12
                }
            ]
        }
        self.client.post("/predict", json=data["flights"])