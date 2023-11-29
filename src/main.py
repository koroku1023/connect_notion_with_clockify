import os
import time
from dotenv import load_dotenv
import requests

# 環境変数を取得
load_dotenv()
CLOCKIFY_API_KEY = os.getenv("CLOCKIFY_API_KEY")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")

def get_clockify_projects():
    """
    ClockifyのProject名とIDを取得する
    """
    url = f"https://api.clockify.me/api/v1/workspaces/{CLOCKIFY_WORKSPACE_ID}/projects"
    headers = {
        "x-api-key": CLOCKIFY_API_KEY
    }
    res = requests.get(url, headers=headers)
    res = res.json()
    project_ids, project_names = [v["id"] for v in res], [v["name"] for v in res]
    return project_ids, project_names

def get_clockify_tasks(project_ids):
    """
    ClockifyのTask名を取得する
    """
    for project_id in project_ids:
        url = f"https://api.clockify.me/api/v1/workspaces/{CLOCKIFY_WORKSPACE_ID}/projects/{project_id}/tasks"
        headers = {
            "x-api-key": CLOCKIFY_API_KEY
        }
        res = requests.get(url, headers=headers)
        res = res.json()
        task_ids, task_names = [v["id"] for v in res], [v["name"] for v in res]
        time.sleep(1)
    return task_ids, task_names

def main():
    # Clockifyについて既存のProjectとTaskを取得
    clockify_project_ids, clockify_project_names = get_clockify_projects()
    clockify_task_ids, clockify_task_names = get_clockify_tasks(clockify_project_ids)
    

if __name__ == "__main__":
    main()