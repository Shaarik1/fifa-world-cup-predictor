from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import pandas as pd
import joblib
from enum import Enum
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# 1. Setup Rate Limiting
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load the Model securely
try:
    model_path = os.path.join("data", "rf_model.joblib")
    encoder_path = os.path.join("data", "team_mapping.joblib")
    
    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)
    print("Security Check: Models loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Model files missing. {e}")
    pass

# 4. Define Valid Teams
class TeamName(str, Enum):
    Algeria = "Algeria"
    Argentina = "Argentina"
    Australia = "Australia"
    Austria = "Austria"
    Belgium = "Belgium"
    Brazil = "Brazil"
    Canada = "Canada"
    CapeVerde = "Cape Verde"
    Colombia = "Colombia"
    Croatia = "Croatia"
    Curacao = "Curaçao"
    Ecuador = "Ecuador"
    Egypt = "Egypt"
    England = "England"
    France = "France"
    Germany = "Germany"
    Ghana = "Ghana"
    Haiti = "Haiti"
    Iran = "Iran"
    IvoryCoast = "Ivory Coast"
    Japan = "Japan"
    Jordan = "Jordan"
    Mexico = "Mexico"
    Netherlands = "Netherlands"
    NewZealand = "New Zealand"
    Panama = "Panama"
    Portugal = "Portugal"
    Qatar = "Qatar"
    SaudiArabia = "Saudi Arabia"
    Scotland = "Scotland"
    SouthAfrica = "South Africa"
    SouthKorea = "South Korea"
    Spain = "Spain"
    Switzerland = "Switzerland"
    Tunisia = "Tunisia"
    UnitedStates = "United States"
    Uruguay = "Uruguay"
    Uzbekistan = "Uzbekistan"

class MatchInput(BaseModel):
    home_team: TeamName
    away_team: TeamName
    neutral_venue: bool = Field(default=False)

    @validator('away_team')
    def teams_must_be_different(cls, v, values):
        if 'home_team' in values and v == values['home_team']:
            raise ValueError('Home and Away teams must be different')
        return v

@app.get("/")
def home():
    return {"message": "FIFA World Cup AI API (Secured)"}

@app.post("/predict")
@limiter.limit("10/minute")
def predict_match(data: MatchInput, request: Request):
    home_team_str = data.home_team.value
    away_team_str = data.away_team.value
    
    # Create DataFrame with initial values
    input_data = pd.DataFrame({
        'home_team': [home_team_str],
        'away_team': [away_team_str],
        'neutral_venue': [data.neutral_venue]
    })
    
    try:
        if hasattr(label_encoder, 'transform'):
            input_data['home_team_encoded'] = label_encoder.transform(input_data['home_team'])
            input_data['away_team_encoded'] = label_encoder.transform(input_data['away_team'])
        else:
            input_data['home_team_encoded'] = input_data['home_team'].map(label_encoder)
            input_data['away_team_encoded'] = input_data['away_team'].map(label_encoder)
            
    except Exception as e:
        print(f"Encoding Error: {e}")
        raise HTTPException(status_code=400, detail="Team encoding failed. Check team names.")
    
    # --- FIX STARTS HERE ---
    # We rename the columns to match EXACTLY what the model expects
    features = input_data[['home_team_encoded', 'away_team_encoded', 'neutral_venue']]
    features.columns = ['home_team_code', 'away_team_code', 'neutral']
    # --- FIX ENDS HERE ---
    
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    return {
        "prediction": prediction,
        "probability": {
            "draw": round(probabilities[0], 2),
            "home_win": round(probabilities[1], 2),
            "away_win": round(probabilities[2], 2)
        },
        "match_info": {
            "home": home_team_str,
            "away": away_team_str,
            "neutral": data.neutral_venue
        }
    }
