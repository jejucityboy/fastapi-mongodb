import motor.motor_asyncio
from pymongo import MongoClient
from decouple import config


def conn():
    MONGO_DETAILS = config("MONGO_DETAILS")
    client = MongoClient(MONGO_DETAILS)
    # client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    database = client.students
    student_collection = database.get_collection("students_collection")
    return student_collection
