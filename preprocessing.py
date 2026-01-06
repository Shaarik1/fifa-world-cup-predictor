import pandas as pd

def load_and_preprocess():
    print("🔄 Loading raw data...")
    # Read the file we just downloaded
    df = pd.read_csv("data/results.csv")
    
    # 1. Convert "date" column to real datetime objects so we can filter by year
    df["date"] = pd.to_datetime(df["date"])
    
    # 2. CREATE TARGET VARIABLE (What we want to predict)
    # The model can't predict "2-1". It predicts: Win (1), Loss (2), or Draw (0).
    # Logic:
    # If Home Score > Away Score -> Home Win (1)
    # If Away Score > Home Score -> Away Win (2)
    # Else -> Draw (0)
    
    def get_match_result(row):
        if row['home_score'] > row['away_score']:
            return 1 # Home Win
        elif row['away_score'] > row['home_score']:
            return 2 # Away Win
        else:
            return 0 # Draw

    df['match_result'] = df.apply(get_match_result, axis=1)

    # 3. ENCODE TEAM NAMES
    # Computers can't read "Brazil". We convert them to ID numbers (Brazil=5, France=22).
    # We use "astype('category').cat.codes" which is a fast way to do this in Pandas.
    df["home_team_code"] = df["home_team"].astype("category").cat.codes
    df["away_team_code"] = df["away_team"].astype("category").cat.codes
    
    # 4. NEUTRAL VENUE
    # In the World Cup, most games are "Neutral" (played in a host country).
    # This removes the "Home Field Advantage" usually seen in club football.
    # We convert True/False to 1/0.
    df["neutral"] = df["neutral"].astype(int)

    # 5. FILTER DATA
    # Football tactics changed heavily over time. Data from 1872 is noise.
    # We will only train on "Modern Era" football (post-1990).
    df_modern = df[df["date"] > "1990-01-01"].copy()
    
    print(f"✅ Preprocessing complete. Training dataset size: {len(df_modern)} matches.")
    
    # Show the balance (Do home teams win more often?)
    print("📊 Win Distribution (1=Home Win, 2=Away Win, 0=Draw):")
    print(df_modern['match_result'].value_counts(normalize=True))

    return df_modern

if __name__ == "__main__":
    data = load_and_preprocess()
    # Save the clean data to a new file
    data.to_csv("data/processed_data.csv", index=False)
    print("💾 Saved clean data to data/processed_data.csv")





