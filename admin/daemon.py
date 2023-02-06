from flask import Flask
from configuration import Configuration
from models import database, Elections, Vote
from sqlalchemy import and_
from redis import Redis
from datetime import datetime, timedelta

application = Flask(__name__)
application.config.from_object(Configuration)
database.init_app(application)

with application.app_context() as context:
    with Redis(host=Configuration.REDIS_HOST) as redis:
        while True:

            data = redis.lpop(Configuration.REDIS_VOTE_LIST)
            if not data:
                continue
            line = data.decode("utf-8").split(",")

            guid = line[0]
            pollNumber = line[1]
            officialJmbg = line[2]

            currDateTime = datetime.now()
            hours = 2
            hoursAdded = timedelta(hours=hours)
            futureDateTime = currDateTime + hoursAdded
            election = Elections.query.filter(and_(Elections.start < futureDateTime, futureDateTime < Elections.end)).first()
            if not election:
                continue

            vote = Vote(ballotGuid=guid, electionOfficialJmbg=officialJmbg, pollNumber=pollNumber, electionId=election.id)
            database.session.add(vote)
            database.session.commit()
