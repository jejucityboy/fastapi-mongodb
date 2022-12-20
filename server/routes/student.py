from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
)
from server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
)

router = APIRouter()

@router.post("/", response_description="학생 추가")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)

    return ResponseModel(new_student, "success")

@router.get("/", response_description="전체 학생 조회")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "success")
    return ResponseModel(students, "empty list...")

@router.get("/{id}", response_description="ID로 학생 조회")
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "success")
    return ErrorResponseModel("An error occurred", 404, "Student doesn't exist.")

@router.get("/{fullname}", response_description="이름으로 학생 조회")
async def get_student_data(fullname):
    student = await retrieve_student(fullname)
    if student:
        return ResponseModel(student, "success")
    return ErrorResponseModel("An error occurred", 404, "Student doesn't exist.")

@router.put("/{id}", response_description="해당 ID의 학생정보 수정")
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            "Student with ID: {} name update is successful".format(id),
            "Student name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )

@router.delete("/{id}", response_description="ID로 학생정보 삭제")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )
