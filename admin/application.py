from datetime import datetime, timedelta
from adminDecorator import roleCheck
from flask import Flask, request, Response, json
from configuration import Configuration
from models import database, Participant, Elections, ElectionParticipants, Vote
from flask_jwt_extended import JWTManager
from dateutil import parser

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)

@application.route("/createParticipant", methods = ["POST"])
@roleCheck(role = "admin")
def createParticipant():

    # if request.json is None:
    #     data = {"message": "Field name is missing."}
    #     json_obj = json.dumps(data, indent=4)
    #     return Response(json_obj, status=400)

    name = request.json.get("name", "")
    individual = request.json.get("individual", None)

    if name != " " and not name:
        data = {"message": "Field name is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    nameEmpty = len(name) == 0

    if nameEmpty:
        data = {"message": "Field name is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if individual is None:
        data = {"message": "Field individual is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    participant = Participant(name=name, individual=individual)
    database.session.add(participant)
    database.session.commit()

    id = participant.id
    data = {"id": id}
    json_obj = json.dumps(data)

    return Response(json_obj, status=200)

@application.route("/getParticipants", methods = ["GET"])
@roleCheck(role = "admin")
def getParticipants():

    participants = Participant.query.all()

    data = []
    for participant in participants:
        data.append(participant.as_dict())

    resp = {
        "participants": data
    }

    return Response(json.dumps(resp, indent=4), status=200)

@application.route("/createElection", methods = ["POST"])
@roleCheck(role = "admin")
def createElection():

    # if request.json is None:
    #     data = {"message": "Field start is missing."}
    #     json_obj = json.dumps(data, indent=4)
    #     return Response(json_obj, status=400)

    start = request.json.get("start", "")
    end = request.json.get("end", "")
    individual = request.json.get("individual", None)
    participantsIDs = request.json.get("participants", None)

    if start != " " and not start:
        data = {"message": "Field start is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if end != " " and not end:
        data = {"message": "Field end is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)


    startEmpty = len(start) == 0
    endEmpty = len(end) == 0

    if startEmpty:
        data = {"message": "Field start is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if endEmpty:
        data = {"message": "Field end is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if individual is None:
        data = {"message": "Field individual is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if participantsIDs is None:
        data = {"message": "Field participants is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)


    try:
        startDate = parser.parse(start)
        endDate = parser.parse(end)
    except:
        data = {"message": "Invalid date and time."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    if endDate <= startDate:
        data = {"message": "Invalid date and time."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    allElections = Elections.query.all()
    electionTmp = Elections(start=startDate, end=endDate, individual=individual)
    database.session.add(electionTmp)
    database.session.commit()
    for election in allElections:
        if election.start < electionTmp.start < election.end:
            data = {"message": "Invalid date and time."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
        if election.start < electionTmp.end < election.end:
            data = {"message": "Invalid date and time."}
            json_obj = json.dumps(data, indent=4)
            return Response(json_obj, status=400)
    database.session.delete(electionTmp)
    database.session.commit()

    if len(participantsIDs) < 2:
        data = {"message": "Invalid participants."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    participants = []
    try:
        for participantID in participantsIDs:
            participant = Participant.query.filter(Participant.id == participantID).first()
            if participant.individual != individual:
                data = {"message": "Invalid participants."}
                json_obj = json.dumps(data, indent=4)
                return Response(json_obj, status=400)
            participants.append(participant)
    except:
        data = {"message": "Invalid participants."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    election = Elections(start=startDate, end=endDate, individual=individual)
    database.session.add(election)
    database.session.commit()

    pollNumber = 1
    for participant in participants:
        electionParticipant = ElectionParticipants(pollNumber = pollNumber, participantId = participant.id, electionId = election.id)
        database.session.add(electionParticipant)
        database.session.commit()
        pollNumber = pollNumber + 1

    data = []
    cnt = 1
    for participant in participants:
        data.append(cnt)
        cnt = cnt + 1

    resp = {
        "pollNumbers": data
    }

    return Response(json.dumps(resp, indent=4), status=200)

@application.route("/getElections", methods = ["GET"])
@roleCheck(role = "admin")
def getElections():

    elections = Elections.query.all()

    data = []
    for election in elections:
        data.append(election.as_dict())

    resp = {
        "elections": data
    }
    return Response(json.dumps(resp, indent=4), status=200)

@application.route("/getResults", methods=["GET"])
@roleCheck(role="admin")
def getResults():

    # if request.args is None:
    #     data = {"message": "Field id is missing."}
    #     json_obj = json.dumps(data, indent=4)
    #     return Response(json_obj, status=400)

    try:
        electionId = int(request.args["id"])
    except:
        data = {"message": "Field id is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    if electionId == "" or electionId == " ":
        data = {"message": "Field id is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)
    if electionId is None:
        data = {"message": "Field id is missing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    election = Elections.query.filter(Elections.id == electionId).first()
    if not election:
        data = {"message": "Election does not exist."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    currDateTime = datetime.now()
    hours = 2
    hoursAdded = timedelta(hours=hours)
    futureDateTime = currDateTime + hoursAdded
    if futureDateTime < election.end:
        data = {"message": "Election is ongoing."}
        json_obj = json.dumps(data, indent=4)
        return Response(json_obj, status=400)

    electionParticipants = ElectionParticipants.query.filter(ElectionParticipants.electionId == electionId).all()

    votes = Vote.query.filter(Vote.electionId == electionId).all()

    dataInvalidVotes = []
    invalidVotes = []
    for vote1 in votes:
        for vote2 in votes:
            if vote1.ballotGuid == vote2.ballotGuid and vote1.id != vote2.id:
                invalidVotes.append(vote2)
                jsonInvalidVote = {
                    "electionOfficialJmbg": vote2.electionOfficialJmbg,
                    "ballotGuid": vote2.ballotGuid,
                    "pollNumber": vote2.pollNumber,
                    "reason": "Duplicate ballot."
                }
                dataInvalidVotes.append(jsonInvalidVote)
                votes.remove(vote2)
        if vote1.pollNumber > len(electionParticipants):
            invalidVotes.append(vote1)
            jsonInvalidVote = {
                "electionOfficialJmbg": vote1.electionOfficialJmbg,
                "ballotGuid": vote1.ballotGuid,
                "pollNumber": vote1.pollNumber,
                "reason": "Invalid poll number."
            }
            dataInvalidVotes.append(jsonInvalidVote)
            votes.remove(vote1)


    votesCount = []
    for i in electionParticipants:
        votesCount.append(0)
    for vote in votes:
        votesCount[vote.pollNumber-1] += 1

    data = []

    if election.individual:
        for electionParticipant in electionParticipants:
            participant = Participant.query.filter(Participant.id == electionParticipant.participantId).first()
            jsonParticipant = {
                "pollNumber": electionParticipant.pollNumber,
                "name": participant.name,
                "result": round(votesCount[electionParticipant.pollNumber-1]/len(votes), 2)
            }
            data.append(jsonParticipant)
    else:
        votesCountInitial = []
        for vote in votesCount:
            votesCountInitial.append(vote)
        validParticipants = []
        for electionParticipant in electionParticipants:
            percent = votesCount[electionParticipant.pollNumber-1]/len(votes)*100
            if percent >= 5:
                validParticipants.append(electionParticipant)
        participantMandates = []
        for validParticipant in electionParticipants:
            participantMandates.append(0)
        for i in range(0, 250):
            maxVotes = 0
            participantPollNumber = 0
            for validParticipant in validParticipants:
                if votesCount[validParticipant.pollNumber-1] > maxVotes:
                    maxVotes = votesCount[validParticipant.pollNumber-1]
                    participantPollNumber = validParticipant.pollNumber
            participantMandates[participantPollNumber-1] += 1
            votesCount[participantPollNumber-1] = votesCountInitial[participantPollNumber-1]/participantMandates[participantPollNumber-1]

        for electionParticipant in electionParticipants:
            isValid = False
            for validParticipant in validParticipants:
                if validParticipant == electionParticipant:
                    isValid = True
            participant = Participant.query.filter(Participant.id == electionParticipant.participantId).first()
            if isValid:
                jsonParticipant = {
                    "pollNumber": electionParticipant.pollNumber,
                    "name": participant.name,
                    "result": participantMandates[electionParticipant.pollNumber-1]
                }
            else:
                jsonParticipant = {
                    "pollNumber": electionParticipant.pollNumber,
                    "name": participant.name,
                    "result": 0
                }
            data.append(jsonParticipant)

    resp = {
        "participants": data,
        "invalidVotes": dataInvalidVotes
    }

    return Response(json.dumps(resp, indent=4), status=200)


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug = True, host="0.0.0.0", port = 5001)
