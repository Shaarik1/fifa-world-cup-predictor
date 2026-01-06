from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, validator
import pandas as pd
import joblib
from enum import Enum
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. Setup Rate Limiting (Identify users by IP address)
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Load the Model securely
# We try/except to ensure the app doesn't crash if files are missing during build
try:
    model = joblib.load("model.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    print("Security Check: Models loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Model files missing. {e}")
    # In production, you might want to exit here, but for now we pass
    pass

# 3. Define Valid Teams (Whitelist)
# This prevents "Prompt Injection" or garbage data.
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

# 4. Input Schema with Validation
class MatchInput(BaseModel):
    home_team: TeamName  # Must be in the Enum list above
    away_team: TeamName  # Must be in the Enum list above
    neutral_venue: bool = Field(default=False)

    # Custom validator to prevent same-team matches
    @validator('away_team')
    def teams_must_be_different(cls, v, values):
        if 'home_team' in values and v == values['home_team']:
            raise ValueError('Home and Away teams must be different')
        return v

@app.get("/")
def home():
    return {"message": "FIFA World Cup AI API (Secured)"}

@app.post("/predict")
@limiter.limit("10/minute") # Security: Rate Limit to 10 requests per minute per IP
def predict_match(data: MatchInput, request: Request):
    # Data is already sanitized and validated by Pydantic at this point
    
    # Convert Enum to string for processing
    home_team_str = data.home_team.value
    away_team_str = data.away_team.value
    
    # Create DataFrame
    input_data = pd.DataFrame({
        'home_team': [home_team_str],
        'away_team': [away_team_str],
        'neutral_venue': [data.neutral_venue]
    })
    
    # Encode teams
    try:
        input_data['home_team_encoded'] = label_encoder.transform(input_data['home_team'])
        input_data['away_team_encoded'] = label_encoder.transform(input_data['away_team'])
    except ValueError:
        # Fallback if a team somehow bypassed validation (unlikely with Enum)
        raise HTTPException(status_code=400, detail="Team not found in training data")
    
    # Prepare features
    features = input_data[['home_team_encoded', 'away_team_encoded', 'neutral_venue']]
    
    # Predict
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
