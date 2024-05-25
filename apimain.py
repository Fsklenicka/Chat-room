from flask import Flask, request, jsonify
import AuthGate

app = Flask(__name__)


@app.route("/get-user/<user_id>/<password>")
def get_user(user_id, password):
    if AuthGate.authuser(username=user_id, password=password):
        return '1', 200
    else:
        return '0', 401

@app.route("/reg-user/<userID>/<password>")
def reg_user(userID, password):
    res = AuthGate.registeruser(username=userID, password=password)
    if res == 1:
        return '1', 201
    else:
        return '0', 400

@app.route("/userlist/get")
def getlist():
    user_list = AuthGate.userlist()
    return jsonify(user_list), 200



if __name__ == '__main__':
    app.run(debug=True,)
