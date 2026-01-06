import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train():
    print("🚀 Loading processed data...")
    df = pd.read_csv("data/processed_data.csv")

    # 1. Define Features (X) and Target (y)
    # X = The things we know before the match (Home Team, Away Team, Neutral Venue)
    # y = The result (Home Win, Away Win, Draw)
    X = df[["home_team_code", "away_team_code", "neutral"]]
    y = df["match_result"]

    # 2. Split Data (80% for training, 20% for testing)
    print("✂️  Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Train the Random Forest
    print("🧠 Training Random Forest Model...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # 4. Evaluate
    predictions = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:\n", classification_report(y_test, predictions))

    # 5. Save the Model
    # We save this so the API can load it without retraining every time.
    joblib.dump(rf_model, "data/rf_model.joblib")
    print("💾 Model saved to data/rf_model.joblib")

    # 6. Save the Team Mappings (CRITICAL STEP)
    # We need to recreate the mapping between "Brazil" and its ID number
    # so our API can translate user input later.
    
    # Reload raw data briefly to get the names
    raw_df = pd.read_csv("data/results.csv")
    # Filter just like we did in preprocessing to be safe (though codes are consistent)
    # Actually, simpler way: The codes in processed_data came from alphabetical sorting usually.
    # Let's rebuild the map safely:
    
    raw_df["home_team_code"] = raw_df["home_team"].astype("category").cat.codes
    
    # Create a dictionary: { "Brazil": 43, "France": 67, ... }
    team_mapping = dict(zip(raw_df["home_team"], raw_df["home_team_code"]))
    
    # Save this dictionary
    joblib.dump(team_mapping, "data/team_mapping.joblib")
    print("💾 Team mapping saved to data/team_mapping.joblib")

if __name__ == "__main__":
    train()
