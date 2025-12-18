import requests
from requests.auth import HTTPBasicAuth

# CONFIG Details
INSTANCE_URL = "https://dev307115.service-now.com"
USERNAME = "admin"
PASSWORD = "=l6Om+bXO2Oq"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

Incident_States = ['New', 'In Progress', 'On Hold', '', '', 'Resolved', 'Closed', 'Cancelled']

AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

def create_ticket(short_desc, description, ticket_type='incident'):  # CREATE INCIDENT
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}"
    payload = {
        "short_description": short_desc,
        "description": description,
        "category": "software",
        "impact": "2",
        "urgency": "2"
    }

    r = requests.post(url, auth=AUTH, headers=HEADERS, json=payload)
    r.raise_for_status()
    result = r.json()["result"]

    print(f"Created {ticket_type}: {result['number']}")
    return result["sys_id"], result["number"]


def get_tickets(ticket_type='incident', limit=5):  # READ INCIDENTS
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}?sysparm_limit={limit}"
    r = requests.get(url, auth=AUTH, headers=HEADERS)
    r.raise_for_status()

    print(f"\n List of {ticket_type}s:")
    for tkt in r.json()["result"]:
        print(f"{tkt['number']} | {tkt['short_description']}")


def update_ticket(sys_id, ticket_type='incident', status='Resolved'):  # UPDATE INCIDENT
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"
    payload = {
        "state": "2",  # In Progress
        "comments": "Work started via Python utility"
    }

    r = requests.patch(url, auth=AUTH, headers=HEADERS, json=payload)
    r.raise_for_status()
    print(f"{ticket_type} {sys_id} is updated")


def get_user_sys_id(username):  # GET USER SYS_ID for Triaging
    url = f"{INSTANCE_URL}/api/now/table/sys_user"
    params = {"sysparm_query": f"user_name={username}"}

    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    r.raise_for_status()

    users = r.json()["result"]
    if not users:
        raise Exception("User not found")

    return users[0]["sys_id"]


def get_group_sys_id(group_name):  # GET GROUP SYS_ID for triaging
    url = f"{INSTANCE_URL}/api/now/table/sys_user_group"
    params = {"sysparm_query": f"name={group_name}"}

    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    r.raise_for_status()

    groups = r.json()["result"]
    if not groups:
        raise Exception("Group not found")

    return groups[0]["sys_id"]


def assign_ticket(sys_id, ticket_type='incident', user_sys_id=None, group_sys_id=None):  # ASSIGN INCIDENT
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"
    payload = {}

    if user_sys_id:
        payload["assigned_to"] = user_sys_id
    if group_sys_id:
        payload["assignment_group"] = group_sys_id

    r = requests.patch(url, auth=AUTH, headers=HEADERS, json=payload)
    r.raise_for_status()
    print(f" {ticket_type} {sys_id} assigned")


def delete_ticket(sys_id, ticket_type='incident'):  # Delete ticket
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"
    r = requests.delete(url, auth=AUTH, headers=HEADERS)
    r.raise_for_status()
    print(f" {ticket_type} {sys_id} deleted")

# code flow starts here


if __name__ == "__main__":
    ticket_type = 'incident'

    try:
        # 1. Create
        sys_id, number = create_ticket(
            "Python ServiceNow Integration",
            "Incident created using Python REST API",
            ticket_type
        )

        # 2. Read
        get_tickets(ticket_type)

        # 3. Update
        update_ticket(sys_id, ticket_type, Incident_States[1])  # In progress

        # 4. Assign to user
        user_sys_id = get_user_sys_id("admin")
        assign_ticket(sys_id, user_sys_id=user_sys_id)

        # 5. Assign to group (auto triaging)
        # group_sys_id = get_group_sys_id("Service Desk")
        # assign_ticket(sys_id, group_sys_id=group_sys_id)

        # 6. Delete (not needed)
        # delete_ticket(sys_id)

    except Exception as e:
        print("Error:", e)
