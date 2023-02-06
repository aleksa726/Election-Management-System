from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class ElectionParticipants(database.Model):
    __tablename__ = "electionParticipants"

    id = database.Column(database.Integer, primary_key = True)
    pollNumber = database.Column(database.Integer, nullable=False)
    participantId = database.Column(database.Integer, database.ForeignKey("participant.id"), nullable = False)
    electionId = database.Column(database.Integer, database.ForeignKey("elections.id"), nullable = False)


class Elections(database.Model):
    __tablename__ = "elections"

    id = database.Column(database.Integer, primary_key = True)
    start = database.Column(database.DateTime, nullable = False)
    end = database.Column(database.DateTime, nullable = False)
    individual = database.Column(database.Boolean, nullable = False)

    participants = database.relationship("Participant", secondary = ElectionParticipants.__table__, back_populates = "elections")

    def as_dict(self):
        electionParticipants = ElectionParticipants.query.filter(ElectionParticipants.electionId == self.id).all()
        participants = []
        for electionParticipant in electionParticipants:
            participant = Participant.query.filter(Participant.id == electionParticipant.participantId).first()
            participants.append(participant.as_dict2())
        return {
            "id": self.id,
            "start": str(self.start),
            "end": str(self.end),
            "individual": self.individual,
            "participants": participants
        }

class Participant(database.Model):
    __tablename__ = "participant"

    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(256), nullable = False)
    individual = database.Column(database.Boolean(1), nullable = False)

    elections = database.relationship("Elections", secondary = ElectionParticipants.__table__, back_populates = "participants");

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "individual": self.individual
        }
    def as_dict2(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Vote(database.Model):

    __tablename__ = "vote"

    id = database.Column(database.Integer, primary_key = True)
    ballotGuid = database.Column(database.String(36), nullable = False)
    electionOfficialJmbg = database.Column(database.String(13), nullable = False)
    pollNumber = database.Column(database.Integer, nullable = False)

    electionId = database.Column(database.Integer, database.ForeignKey("elections.id"), nullable = False)
