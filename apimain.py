from flask import Flask, request, jsonify
import AuthGate
import Emails

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

@app.route('/chkusr/<UserID>')
def checkusername(UserID):
    res = AuthGate.checkuser(username=UserID)
    if res:
        return '1', 200
    else:
        return '0', 403

@app.route("/userlist/get")
def getlist():
    user_list = AuthGate.userlist()
    return jsonify(user_list), 200

@app.route('/emails/save/<UserID>/<email>')
def saveEmail(UserID, email):
    status = Emails.registeremail(username=UserID, email=email)
    if status:
        return '1', 200

@app.route('/class/get/<UserID>')
def getclass(UserID):
    pass
@app.route('/emails/get/<UserID>')
def getEmail(UserID):
    return Emails.getemail(username=UserID), 200

@app.route('/changepassword/<UserID>/<password>')
def changepassword(UserID, password):
    res = AuthGate.changepassword(username=UserID, password=password)
    if res == True:
        return '1', 200
    else:
        return '0', 400

if __name__ == '__main__':
    app.run(debug=True, host='89.203.249.186')
