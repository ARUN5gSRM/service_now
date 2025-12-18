import requests
from requests.auth import HTTPBasicAuth
from django.shortcuts import render, redirect
from django.contrib import messages


INSTANCE_URL = "https://dev307115.service-now.com"
USERNAME = "admin"
PASSWORD = "=l6Om+bXO2Oq"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

Incident_States = [
    'New',
    'In Progress',
    'On Hold',
    '',
    '',
    'Resolved',
    'Closed',
    'Cancelled'
]

AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


def create_ticket(short_desc, description, ticket_type='incident'):
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

    return result["sys_id"], result["number"]


def get_tickets(ticket_type='incident', limit=50):
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}"

    params = {
        "sysparm_limit": limit,
        "sysparm_query": "ORDERBYDESCsys_created_on",
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true"
    }

    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    r.raise_for_status()

    return r.json()["result"]


def get_ticket_by_sys_id(sys_id, ticket_type='incident'):

    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"

    params = {
        "sysparm_display_value": "false",
        "sysparm_exclude_reference_link": "true"
    }

    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    r.raise_for_status()

    return r.json()["result"]


def update_ticket(sys_id, status, ticket_type='incident'):
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"

    payload = {
        "state": str(status),
        "comments": "Updated via Django UI"
    }

    r = requests.patch(url, auth=AUTH, headers=HEADERS, json=payload)
    r.raise_for_status()


def get_user_sys_id(username):
    url = f"{INSTANCE_URL}/api/now/table/sys_user"
    params = {
        "sysparm_query": f"user_name={username}",
        "sysparm_limit": 1
    }

    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    r.raise_for_status()

    users = r.json()["result"]
    return users[0]["sys_id"] if users else None


def get_group_sys_id(group_name):
    url = f"{INSTANCE_URL}/api/now/table/sys_user_group"
    params = {
        "sysparm_query": f"name={group_name}",
        "sysparm_limit": 1
    }

    r = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    r.raise_for_status()

    groups = r.json()["result"]
    return groups[0]["sys_id"] if groups else None


def assign_ticket(sys_id, ticket_type='incident', user_sys_id=None, group_sys_id=None):
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"
    payload = {}

    if user_sys_id:
        payload["assigned_to"] = user_sys_id
    if group_sys_id:
        payload["assignment_group"] = group_sys_id

    r = requests.patch(url, auth=AUTH, headers=HEADERS, json=payload)
    r.raise_for_status()


def delete_ticket(sys_id, ticket_type='incident'):
    url = f"{INSTANCE_URL}/api/now/table/{ticket_type}/{sys_id}"
    r = requests.delete(url, auth=AUTH, headers=HEADERS)
    r.raise_for_status()


def create_ticket_view(request):
    if request.method == "POST":
        short_desc = request.POST["short_desc"]
        description = request.POST["description"]

        sys_id, number = create_ticket(short_desc, description)
        messages.success(request, f"Incident {number} created successfully")
        return redirect("list")

    return render(request, "incidents/create_ticket.html")


def list_tickets_view(request):
    tickets = get_tickets()
    return render(request, "incidents/list_tickets.html", {"tickets": tickets})


def update_ticket_view(request, sys_id):
    if request.method == "POST":
        state = int(request.POST["state"])
        update_ticket(sys_id, status=state)

        messages.success(request, "Incident updated successfully")
        return redirect("list")

    incident = get_ticket_by_sys_id(sys_id)

    return render(
        request,
        "incidents/update_ticket.html",
        {
            "sys_id": sys_id,
            "states": enumerate(Incident_States, start=1),
            "current_state": int(incident["state"])
        }
    )


def assign_user_view(request, sys_id):
    if request.method == "POST":
        username = request.POST["username"]

        user_sys_id = get_user_sys_id(username)
        if not user_sys_id:
            messages.error(request, f"User '{username}' not found in ServiceNow")
            return redirect(request.path)

        assign_ticket(sys_id, user_sys_id=user_sys_id)
        messages.success(request, f"Assigned to user {username}")
        return redirect("list")

    return render(request, "incidents/assign_user.html", {"sys_id": sys_id})


def assign_group_view(request, sys_id):
    if request.method == "POST":
        group = request.POST["group"]

        group_sys_id = get_group_sys_id(group)
        if not group_sys_id:
            messages.error(request, f"Group '{group}' not found in ServiceNow")
            return redirect(request.path)

        assign_ticket(sys_id, group_sys_id=group_sys_id)
        messages.success(request, f"Assigned to group {group}")
        return redirect("list")

    return render(request, "incidents/assign_group.html", {"sys_id": sys_id})


def delete_ticket_view(request, sys_id):
    delete_ticket(sys_id)
    messages.success(request, "Incident deleted successfully")
    return redirect("list")
