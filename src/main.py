import os
import time
from dotenv import load_dotenv
import requests

# 環境変数を取得
load_dotenv()
CLOCKIFY_API_KEY = os.getenv("CLOCKIFY_API_KEY")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PROJECT_DB_ID = os.getenv("NOTION_PROJECT_DB_ID")
NOTION_TASK_DB_ID = os.getenv("NOTION_TASK_DB_ID")

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

def get_notion_projects():
    """
    NotionのProject名とIDを取得する
    """
    url = f"https://api.notion.com/v1/databases/{NOTION_PROJECT_DB_ID}/query"
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": "Bearer " + NOTION_API_KEY
    }
    res = requests.post(url, headers=headers)
    res = res.json()
    project_ids, project_names = (
        [result["properties"]["Name"]["title"][0]["plain_text"] for result in res["results"]],
        [result["id"] for result in res["results"]]
    )
    return project_ids, project_names

def get_notion_tasks():
    """
    NotionのTask名とIDを取得する
    """
    url = f"https://api.notion.com/v1/databases/{NOTION_TASK_DB_ID}/query"
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": "Bearer " + NOTION_API_KEY
    }
    res = requests.post(url, headers=headers)
    res = res.json()
    task_ids, task_names, parent_project_names = (
        [result["properties"]["Task"]["title"][0]["plain_text"] for result in res["results"]],
        [result["id"] for result in res["results"]],
        [result["properties"]["Project"]["relation"][0]["id"] for result in res["results"] if len(result["properties"]["Project"]["relation"])!=0]
    )
    return task_ids, task_names, parent_project_names

def main():
    # Clockifyについて既存のProjectとTaskを取得
    clockify_project_ids, clockify_project_names = get_clockify_projects()
    clockify_task_ids, clockify_task_names = get_clockify_tasks(clockify_project_ids)
    
    # Notionについて既存のProjectとTaskを取得
    notion_project_ids, notion_project_names = get_notion_projects()
    notion_task_ids, notion_task_names, notion_parent_project_ids = get_notion_tasks()
    

if __name__ == "__main__":
    main()