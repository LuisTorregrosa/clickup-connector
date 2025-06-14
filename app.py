from flask import Flask, jsonify, send_from_directory, make_response
import requests
import os

print("Flask app is starting...")

app = Flask(__name__)

CLICKUP_API_TOKEN = "pk_206427727_DEJPYO6O0KD9Y86XL3T3E4NJP4MKO3UR"  # Replace this with your real token
CLICKUP_BASE_URL = "https://api.clickup.com/api/v2"

@app.route("/.well-known/ai-plugin.json")
def serve_manifest():
    print("Serving ai-plugin.json (no cache)...")
    response = make_response(send_from_directory(".well-known", "ai-plugin.json", mimetype="application/json"))
    response.headers["Cache-Control"] = "no-store"
    response.headers["Access-Control-Allow-Origin"] = "*"  # <-- ADD THIS LINE
    return response

@app.route("/openapi.json")
def serve_openapi():
    response = make_response(send_from_directory(".", "openapi.json", mimetype="application/json"))
    response.headers["Access-Control-Allow-Origin"] = "*"  # <-- ADD THIS LINE
    return response

@app.route("/.well-known/mcp.json")
def serve_mcp():
    response = make_response(
        send_from_directory(".well-known", "mcp.json", mimetype="application/json")
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/tasks", methods=["GET"])
def get_tasks():
    headers = {
        "Authorization": CLICKUP_API_TOKEN
    }

    # 1. Get your Team ID
    team_response = requests.get(f"{CLICKUP_BASE_URL}/team", headers=headers)
    team_id = team_response.json()["teams"][0]["id"]

    # 2. Get the first Space ID
    space_response = requests.get(f"{CLICKUP_BASE_URL}/team/{team_id}/space", headers=headers)
    space_id = space_response.json()["spaces"][0]["id"]

    # 3. Get the first Folder ID
    folder_response = requests.get(f"{CLICKUP_BASE_URL}/space/{space_id}/folder", headers=headers)
    folder_id = folder_response.json()["folders"][0]["id"]

    # 4. Get the first List ID
    list_response = requests.get(f"{CLICKUP_BASE_URL}/folder/{folder_id}/list", headers=headers)
    list_id = list_response.json()["lists"][0]["id"]

    # 5. Get the tasks
    tasks_response = requests.get(f"{CLICKUP_BASE_URL}/list/{list_id}/task", headers=headers)
    return jsonify(tasks_response.json())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", debug=True, port=port)