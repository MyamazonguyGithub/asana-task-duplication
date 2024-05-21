import time
import requests
from functools import wraps
import json
import os
from dotenv import load_dotenv

load_dotenv('C:\\Users\\Ozild\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\Code\\Duplicate Task\\asana-task-duplication.env')

hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
asana_access_token = os.getenv('ASANA_ACCESS_TOKEN')

asana_headers = {
    "Authorization": "Bearer " + asana_access_token,
    "Content-Type": "application/json"
}

hubspot_headers = {
    "Authorization": "Bearer " + hubspot_api_key,
    "Content-Type": "application/json"
}

# This function handles API request retries, ensuring that temporary issues don't halt the entire process, using delay and backoff method.
def retry(attempts=5, delay=1, backoff=2):
    def retry_decorator(func):
        @wraps(func)
        def func_with_retry(*args, **kwargs):
            local_attempts, local_delay = attempts, delay
            while local_attempts > 1:
                try:
                    result = func(*args, **kwargs)
                    if isinstance(result, requests.Response):
                        result.raise_for_status()
                    return result
                except requests.exceptions.HTTPError as e:
                    print(f"Request failed, retrying in {local_delay} seconds...")
                    time.sleep(local_delay)
                    local_attempts -= 1
                    local_delay *= backoff
            return func(*args, **kwargs)  # Last attempt without catching exceptions
        return func_with_retry
    return retry_decorator

# This function retrieves the current clients from the HubSpot API, providing the necessary data to identify the corresponding projects in Asana and update task name to reflect client identity
@retry(attempts=5, delay=2, backoff=2)
def get_current_clients():
    offset = 0
    url = "https://api.hubapi.com/crm/v3/objects/companies/search"
    clients = []
    while True:
        body = json.dumps({
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "lifecyclestage",
                            "operator": "IN",
                            "values": ["45633643","45777159"]
                        },
                        {
                            "propertyName": "client_status",
                            "operator": "EQ",
                            "value": "Active"
                        }
                    ]
                }
            ],
            "properties": ["asana_project", "name"],
            "limit": 100,
            "after": offset
        })
        response = requests.post(url, headers=hubspot_headers, data=body)
        response_json = response.json()
        clients.extend(response_json['results'])
        if response_json.get('paging'):
            offset = response_json['paging']['next']['after']
        else:
            return clients
            # Returns the 'clients' list, which contains the client data retrieved from the API. Each element in the list is a dictionary representing a client, with keys for different client properties.
clients = get_current_clients()
print(clients)


# This function retrieves the details of a specified project in Asana using the Asana API. The project is specified by its unique identifier (GID), which is obtained from the client data retrieved from the HubSpot API.@retry(attempts=5, delay=2, backoff=2)
def get_project(project_gid):
    url = f"https://app.asana.com/api/1.0/projects/{project_gid}"
    response = requests.get(url, headers=asana_headers)
    resp_json = response.json()
    return resp_json['data']
    # Returns the 'data' field from the API response. For a successful get_project request, this would contain details of the project (like name, owner, etc.). In case of an error, 'data' might be missing or contain error details.



# This function creates a duplicate of a specified task in Asana using the Asana API. The duplicated task is then ready for association with each client's project.
@retry(attempts=5, delay=2, backoff=2)
def duplicate_checkin_task(name):
    url = "https://app.asana.com/api/1.0/tasks/1207238712672804/duplicate"
    data = json.dumps({
        "data": {
            "name": f"{name} Advertising Check-in",
            "include": "notes,dates"
        }
    })
    response = requests.post(url, headers=asana_headers, data=data)
    resp_json = response.json()
    return resp_json['data'] 
    # Returns the 'data' field from the API response. For a successful duplicate_checkin_task request, this would contain details of the duplicated task. In case of an error, 'data' might be missing or contain error details.



# This function associates the previously duplicated task with a specified project in Asana using the Asana API. The project is specified by its unique identifier (GID), which is obtained from the corresponding client data retrieved from the HubSpot API.
@retry(attempts=5, delay=2, backoff=2)
def add_project(task, project):
    url = f"https://app.asana.com/api/1.0/tasks/{task}/addProject"
    data = json.dumps({
        "data": {
            "project": project
        }
    })
    response = requests.post(url, headers=asana_headers, data=data)
    resp_json = response.json()
    print(resp_json) 
    # prints the API response, which could include an error if the HubSpot GID is not found in Asana



# This section orchestrates the overall process. It uses the 'get_current_clients' function to retrieve the current clients, identifies the corresponding projects in Asana using the 'get_project' function, duplicates a task using the 'duplicate_checkin_task' function, and then associates the duplicated task with each client's project using the 'add_project' function.
def main():
    clients = get_current_clients()
    for client in clients:
        asana_project = client['properties']['asana_project']
        if not asana_project:
            continue
        asana_project_gid = asana_project.split("/")[-2]
        #client_task = duplicate_checkin_task(client['properties']['name'])
        #client_task_gid = client_task['new_task']['gid']
        #add_project(client_task_gid, asana_project_gid)

        



