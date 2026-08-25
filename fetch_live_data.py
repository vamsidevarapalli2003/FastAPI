"""Fetch live todos/users from the deployed app via HTTPS and save locally."""
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

APP_URL = os.environ.get("APP_URL", "https://fastapi-deployment-n4ix.onrender.com").rstrip("/")
USERNAME = "vamsi163"
PASSWORD = "Vamsi1@2003"


def get_token():
    data = urllib.parse.urlencode({"username": USERNAME, "password": PASSWORD}).encode()
    req = urllib.request.Request(f"{APP_URL}/auth/token", data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["access_token"]


def get_json(path, token):
    req = urllib.request.Request(f"{APP_URL}{path}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main():
    if not (APP_URL and USERNAME and PASSWORD):
        print("Set APP_URL, ADMIN_USERNAME, ADMIN_PASSWORD environment variables first.")
        return 1

    try:
        token = get_token()
        todos = get_json("/admin/todo", token)
        users = get_json("/admin/users", token)
    except urllib.error.HTTPError as e:
        print(f"Request failed: {e.code} {e.read().decode()}")
        return 1

    with open("live_todos.json", "w") as f:
        json.dump(todos, f, indent=2)
    with open("live_users.json", "w") as f:
        json.dump(users, f, indent=2)

    print(f"Saved {len(todos)} todos to live_todos.json")
    print(f"Saved {len(users)} users to live_users.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
