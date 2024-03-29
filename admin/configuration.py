import os

databaseUrl = os.environ["DATABASE_URL"]

class Configuration():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/electionsDatabase"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    REDIS_HOST = "redis"
    REDIS_VOTE_LIST = "votes"
