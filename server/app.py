from fastapi import FastAPI

from server.routes.student import router as StudentRouter
from server.routes.graphql import graphql_app as GraphQLRouter

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(GraphQLRouter, tags=["GraphQL"], prefix="/graphql")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:9000",
    "http://localhost:9999",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}