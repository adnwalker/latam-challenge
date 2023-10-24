import fastapi
from typing import List, Dict, Union
from challenge.model import DelayModel
#from model import DelayModel
from fastapi import HTTPException

import pandas as pd

app = fastapi.FastAPI()
model = DelayModel()

# List of expected feature names
EXPECTED_FEATURES = [
    "OPERA_Latin American Wings",
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]

@app.get("/", response_model=dict)
async def read_root():
    return {"message": "Welcome to the FastAPI LATAM app!"}

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flights: List[Dict[str, Union[str, int]]]) -> dict:
    predictions = []
    errors = []
    for flight in flights:
        try:
            # Create a DataFrame with expected features and fill with zeros
            processed_data = pd.DataFrame(data=0, index=[0], columns=EXPECTED_FEATURES)

            # Update DataFrame with features from the input JSON request
            for key, value in flight.items():
                feature_name = f"{key}_{value}"
                if feature_name in processed_data.columns:
                    processed_data.at[0, feature_name] = 1  # Set the corresponding feature to 1
                else:
                    # If the feature_name is not in EXPECTED_FEATURES, raise an HTTPException with status code 400
                    raise HTTPException(status_code=400, detail=f"Unknown column: {feature_name}")

            # Make predictions
            prediction = model.predict(processed_data)
            predictions.append(prediction[0])

        except Exception as e:
            print(str(e))
            errors.append(f"Invalid input for flight {flight}: {str(e)}")

    if errors:
        # If there are errors, return a 400 status code with error details
        raise HTTPException(status_code=400, detail={"errors": errors})

    return {"predict": predictions}