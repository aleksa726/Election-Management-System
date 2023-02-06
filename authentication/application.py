from flask import Flask, request, Response, jsonify, json
from configuration import Configuration
from models import database, User, UserRole
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_
from adminDecorator import roleCheck

application = Flask(__name__)
application.config.from_object(Configuration )

@application.route("/register", methods = ["POST"])
def register():

    jmbg = request.json.get("jmbg", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    if jmbg != " " and not jmbg:
        data = {"message": "Field jmbg is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if forename != " " and not forename:
        data = {"message": "Field forename is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if surname != " " and not surname:
        data = {"message": "Field surname is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if email != " " and not email:
        data = {"message": "Field email is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if password != " " and not password:
        data = {"message": "Field password is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    jmbgEmpty = len(jmbg) == 0 and jmbg != " "
    forenameEmpty = len(forename) == 0 and forename != " "
    surnameEmpty = len(surname) == 0 and surname != " "
    emailEmpty = len(email) == 0 and email != " "
    passwordEmpty = len(password) == 0 and password != " "

    if jmbgEmpty:
        data = {"message": "Field jmbg is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if forenameEmpty:
        data = {"message": "Field forename is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if surnameEmpty:
        data = {"message": "Field surname is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if emailEmpty:
        data = {"message": "Field email is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if passwordEmpty:
        data = {"message": "Field password is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    if len(jmbg)==13:
        dd = int(jmbg[0:2])
        mm = int(jmbg[2:4])
        yyy = int(jmbg[4:7])
        rr = int(jmbg[7:9])
        bbb = int(jmbg[9:12])
        K = int(jmbg[12])

        if dd < 1 or dd > 31:
            data = {"message": "Invalid jmbg."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        if mm < 1 or mm > 12:
            data = {"message": "Invalid jmbg."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        if yyy < 0 or yyy > 999:
            data = {"message": "Invalid jmbg."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        if rr < 70 or rr > 99:
            data = {"message": "Invalid jmbg."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        if dd < 1 or dd > 31:
            data = {"message": "Invalid jmbg."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        if bbb < 0 or bbb > 999:
            data = {"message": "Invalid jmbg."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)

        a = int(jmbg[0])
        b = int(jmbg[1])
        c = int(jmbg[2])
        d = int(jmbg[3])
        e = int(jmbg[4])
        f = int(jmbg[5])
        g = int(jmbg[6])
        h = int(jmbg[7])
        i = int(jmbg[8])
        j = int(jmbg[9])
        k = int(jmbg[10])
        ll = int(jmbg[11])

        m = 11-((7*(a + g) + 6*(b + h) + 5*(c + i) + 4*(d + j) + 3*(e + k) + 2*(f + ll)) % 11)

        if m < 10:
            if K != m:
                data = {"message": "Invalid jmbg."}
                json_obj = json.dumps(data, indent=4)
                return Response(json_obj, status=400)
        else:
            if K != 0:
                data = {"message": "Invalid jmbg."}
                json_obj = json.dumps(data, indent=4)
                return Response(json_obj, status=400)
    else:
        data = {"message": "Invalid jmbg."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    try:
        result = email.split('@')
        if (len(result[0]) == 0) or (len(result[1]) == 0):
            data = {"message": "Invalid email."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        result2 = result[1].split('.')
        if (len(result2[0]) == 0) or (len(result2[1]) < 2):
            data = {"message": "Invalid email."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
    except:
        data = {"message": "Invalid email."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    if len(password) < 8:
        data = {"message": "Invalid password."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    lower = False
    upper = False
    digit = False
    for letter in password:
        if letter.islower():
            lower = True
        if letter.isupper():
            upper = True
        if letter.isdigit():
            digit = True
    if not(digit and upper and lower):
        data = {"message": "Invalid password."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    user = User.query.filter(User.email == email).first()

    if user:
        data = {"message": "Email already exists."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    user = User(email = email, password = password, forename = forename, surname = surname, jmbg = jmbg)
    database.session.add(user)
    database.session.commit()

    userRole = UserRole(userId=user.id, roleId=2)
    database.session.add(userRole)
    database.session.commit()

    return Response("", status = 200)

jwt = JWTManager(application)

@application.route("/login", methods = ["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    if email != " " and not email:
        data = {"message": "Field email is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if password != " " and not password:
        data = {"message": "Field password is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    emailEmpty = len(email) == 0 and email != " "
    passwordEmpty = len(password) == 0 and password != " "

    if emailEmpty:
        data = {"message": "Field email is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if passwordEmpty:
        data = {"message": "Field password is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    try:
        result = email.split('@')
        if ((len(result[0]) == 0) or (len(result[1]) == 0)):
            data = {"message": "Invalid email."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        result2 = result[1].split('.')
        if ((len(result2[0]) == 0) or (len(result2[1]) < 2)):
            data = {"message": "Invalid email."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
    except:
        data = {"message": "Invalid email."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if ( not user ):
        data = {"message": "Invalid credentials."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status = 400)


    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "jmbg": user.jmbg,
        "roles": [str(role) for role in user.roles]
    }

    accessToken = create_access_token(identity = user.email, additional_claims = additionalClaims)
    refreshToken = create_refresh_token(identity = user.email, additional_claims = additionalClaims)

    data = {
        "accessToken": accessToken,
        "refreshToken": refreshToken
    }
    json_obj = json.dumps(data, indent=4)
    return Response(json_obj, status=200)


@application.route("/refresh", methods = ["POST"])
@jwt_required(refresh = True)
def refresh():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "roles": refreshClaims["roles"]
    }

    accessToken = create_access_token(identity = identity, additional_claims = additionalClaims)
    data = {
        "accessToken": accessToken
    }
    json_obj = json.dumps(data, indent=4)
    return Response(json_obj, status=200)


@application.route("/delete", methods = ["POST"])
@roleCheck(role = "admin")
def delete():

    email = request.json.get("email", "")

    if email != " " and not email:
        data = {"message": "Field email is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    emailEmpty = len(email) == 0 and email != " "

    if emailEmpty:
        data = {"message": "Field email is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    try:
        result = email.split('@')
        if ((len(result[0]) == 0) or (len(result[1]) == 0)):
            data = {"message": "Invalid email."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        result2 = result[1].split('.')
        if ((len(result2[0]) == 0) or (len(result2[1]) < 2)):
            data = {"message": "Invalid email."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
    except:
        data = {"message": "Invalid email."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    user = User.query.filter(User.email == email).first()

    if user:
        userRole = UserRole.query.filter(UserRole.userId == user.id).first();
        database.session.delete(user)
        database.session.delete(userRole)
        database.session.commit()
        return Response("", status = 200)

    data = {"message": "Unknown user."}
    json_obj = json.dumps(data, indent=4)
    return Response(json_obj, status=400)

@application.route("/", methods = ["GET"])
def index():
    return "Hello world!"

if ( __name__ == "__main__" ):
    database.init_app(application)
    application.run(debug = True, host="0.0.0.0", port = 5002)