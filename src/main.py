import os
from dotenv import load_dotenv
import requests

# 環境変数を取得
load_dotenv()
CLOCKIFY_API_KEY = os.getenv("CLOCKIFY_API_KEY")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")

def get_clockify_projects():
    """
    ClockifyのProject名を取得する
    """
    url = f"https://api.clockify.me/api/v1/workspaces/{CLOCKIFY_WORKSPACE_ID}/projects"
    headers = {
        "x-api-key": CLOCKIFY_API_KEY
    }
    res = requests.get(url, headers=headers)
    res = res.json()
    project_names = [v["name"] for v in res]
    return project_names

def main():
    project_names = get_clockify_projects()
    

if __name__ == "__main__":
    main()