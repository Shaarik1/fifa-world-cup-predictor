import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Authenticate using the Environment Variables you set earlier
api = KaggleApi()
api.authenticate()

DATASET_SLUG = "martj42/international-football-results-from-1872-to-2017"
DOWNLOAD_PATH = "./data"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

print(f"🚀 Downloading {DATASET_SLUG}...")
api.dataset_download_files(DATASET_SLUG, path=DOWNLOAD_PATH, unzip=True)
print("✅ Download and extraction complete.")