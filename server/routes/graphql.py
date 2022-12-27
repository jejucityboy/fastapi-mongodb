import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import Body
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
import motor.motor_asyncio
from pymongo import MongoClient
from decouple import config
import json
from pydantic import BaseModel, EmailStr, Field
from typing import List

MONGO_DETAILS = config("MONGO_DETAILS")

client = MongoClient(MONGO_DETAILS)
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")

def student_helper(student) -> dict:

    data = {
        "_id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }

    return json.dumps(data)

@strawberry.type
class Student:
    # _id: str
    fullname: str
    email: str
    # course_of_study: str
    # year: int
    # GPA: float

@strawberry.type
class Query:
    # @strawberry.field
    # def get_students(_id: str) -> Student:
    #
    #     student = student_collection.find_one({"_id": ObjectId(_id)})
    #         if student:
    #
    #     return Student(fullname=fullname, email=email)

    @strawberry.field
    def get_students() -> List[str]:
        students = []
        for student in student_collection.find():
            students.append(student_helper(student))
        return students

@strawberry.type
class Mutation:

    @strawberry.field
    def add_student(fullname: str, email: str, course_of_study: str, year: int, gpa: float) -> str:

        student_data = {"fullname":fullname, "email":email, "course_of_study":course_of_study, "year":year, "gpa":gpa}
        student = student_collection.insert_one(student_data)
        new_student = student_collection.find_one({"_id": student.inserted_id})
        return student_helper(new_student)

    @strawberry.field
    def delete_student(_id: str) -> str:

        student = student_collection.find_one({"_id": ObjectId(_id)})
        if student:
            student_collection.delete_one({"_id": ObjectId(_id)})
            return "학생 ID: {} 삭제 완료".format(_id)
        return "학생 ID: {} 존재하지 않음".format(_id)

    # @strawberry.field
    # def update_student(_id: str, fullname: str, email: str, course_of_study: str, year: int, gpa: float) -> str:
    #


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)