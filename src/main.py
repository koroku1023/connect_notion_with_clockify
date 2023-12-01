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
    task_ids = []
    task_names = []
    for project_id in project_ids:
        url = f"https://api.clockify.me/api/v1/workspaces/{CLOCKIFY_WORKSPACE_ID}/projects/{project_id}/tasks"
        headers = {
            "x-api-key": CLOCKIFY_API_KEY
        }
        res = requests.get(url, headers=headers)
        res = res.json()
        task_ids += [v["id"] for v in res]
        task_names += [v["name"] for v in res]
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
        [result["id"] for result in res["results"]],
        [result["properties"]["Name"]["title"][0]["plain_text"] for result in res["results"]]
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
    payload = {
        "filter": {
            "property": "Done",
            "checkbox": {
                "equals": False
            }
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    res = res.json()
    task_ids, task_names, parent_project_names = (
        [result["id"] for result in res["results"]],
        [result["properties"]["Task"]["title"][0]["plain_text"] for result in res["results"]],
        [result["properties"]["Project"]["relation"][0]["id"] for result in res["results"] if len(result["properties"]["Project"]["relation"])!=0]
    )
    return task_ids, task_names, parent_project_names

def add_clockify_new_project(project_name):
    """
    Clockifyの新しいProjectを作成する
    """
    url = f"https://api.clockify.me/api/v1/workspaces/{CLOCKIFY_WORKSPACE_ID}/projects"
    headers = {
        "x-api-key": CLOCKIFY_API_KEY
    }
    json_data = {
        "name": project_name,
        "isPublic": False,
        "public": False
    }
    res = requests.post(url, headers=headers, json=json_data)
    
def add_clockify_new_task(project_id, task_name):
    """
    Clockifyの新しいTaskを作成する
    """
    url = f"https://api.clockify.me/api/v1/workspaces/{CLOCKIFY_WORKSPACE_ID}/projects/{project_id}/tasks"
    headers = {
        "x-api-key": CLOCKIFY_API_KEY
    }
    json_data = {
        "name": task_name,
        "statusEnum": "ACTIVE"
    }
    res = requests.post(url, headers=headers, json=json_data)

def main():
    # Clockifyについて既存のProjectとTaskを取得
    clockify_project_ids, clockify_project_names = get_clockify_projects()
    clockify_task_ids, clockify_task_names = get_clockify_tasks(clockify_project_ids)
    clockify_project_dic = {name: id for name, id in zip(clockify_project_names, clockify_project_ids)}
    
    # Notionについて既存のProjectとTaskを取得
    notion_project_ids, notion_project_names = get_notion_projects()
    notion_project_dic = {id: name for id, name in zip(notion_project_ids, notion_project_names)}
    notion_task_ids, notion_task_names, notion_parent_project_ids = get_notion_tasks()
    
    # 新しいProjectをClockifyにも作成
    for notion_project_name in notion_project_names:
        if notion_project_name not in clockify_project_names:
            add_clockify_new_project(notion_project_name)
    
    # 新しいTaskをClockifyにも作成
    for notion_task_name, notion_project_id in zip(notion_task_names, notion_parent_project_ids):
        if notion_task_name not in clockify_task_names:
            notion_project_name = notion_project_dic[notion_project_id]
            clockify_project_id = clockify_project_dic[notion_project_name]
            add_clockify_new_task(clockify_project_id, notion_task_name)
            break

if __name__ == "__main__":
    main()