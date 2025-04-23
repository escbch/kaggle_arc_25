import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_data(competition_name: str = "arc-prize-2025", download_dir: str = "./arc2025_data"):
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_json_path):
        raise FileNotFoundError("kaggle.json not found. Place the file in ~/.kaggle/")

    api = KaggleApi()
    api.authenticate()

    os.makedirs(download_dir, exist_ok=True)

    print(f"Downloading dataset for competition: {competition_name}")
    api.competition_download_files(competition_name, path=download_dir)

    zip_path = os.path.join(download_dir, f"{competition_name}.zip")
    if os.path.exists(zip_path):
        print("Extracting dataset...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
        print("Extraction completed.")
    else:
        print("Zip file not found. Something went wrong during download.")