from flask import Flask, request, Response, json
from configuration import Configuration
from models import database, Vote
from adminDecorator import roleCheck
from flask_jwt_extended import JWTManager, get_jwt
import io
import csv
from redis import Redis

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)

@application.route("/vote", methods=["POST"])
@roleCheck(role="user")
def vote():
    try:
        file = request.files["file"].stream.read().decode("utf-8")
    except:
        data = {"message": "Field file is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if not file:
        data = {"message": "Field file is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    stream = io.StringIO(file)
    reader = csv.reader(stream)

    votes = []
    cnt = 0
    for row in reader:
        if len(row) != 2:
            msg = "Incorrect number of values on line " + str(cnt) + "."
            data = {"message": msg}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        try:
            if int(row[1]) <= 0:
                msg = "Incorrect poll number on line " + str(cnt) + "."
                data = {"message": msg}
                json_obj = json.dumps(data, indent=4)
                return Response(json_obj, status=400)
        except:
            msg = "Incorrect poll number on line " + str(cnt) + "."
            data = {"message": msg}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        guid = row[0]
        pollNumber = row[1]
        votes.append(guid + "," + str(pollNumber))
        cnt += 1

    jmbg = get_jwt()["jmbg"]

    with Redis(host=Configuration.REDIS_HOST) as re:
        for vote in votes:
            vote = vote + "," + jmbg
            re.rpush(Configuration.REDIS_VOTE_LIST, vote)

    return Response("", status = 200)


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug = True, host="0.0.0.0", port = 5003)