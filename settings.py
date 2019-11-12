# settings.py
from dotenv import load_dotenv
import os
load_dotenv()

load_dotenv(verbose=True)

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

HARVEST_ACCESS_TOKEN = os.getenv("HARVEST_ACCESS_TOKEN")
HARVEST_ACCOUNT_ID = os.getenv("HARVEST_ACCOUNT_ID")

BASE_URL = "https://api.harvestapp.com/v2/"
USER_URL = BASE_URL+"users/me"
PROJECT_URL = BASE_URL+"users/{user_id}/project_assignments"
TIME_URL = BASE_URL+"time_entries"
