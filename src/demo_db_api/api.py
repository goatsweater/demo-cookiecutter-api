import uuid
from importlib.metadata import version

from fastapi import FastAPI, RequestValidationError

from .schemas import response

app = FastAPI(
    title="Demo cookiecutter API",
    description="Demo of an API. Created from the StatCan datascience-cookiecutter.",
    version=version("demo_db_api"),
    license_info={
        "name": "MIT",
        "url": "https://github.com/goatsweater/demo-cookiecutter-api/blob/main/LICENSE"
    }
)


#####
# Response message for validation errors
#####
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    err = response.Error(
        code=exc.status_code,
        detail=str(exc.detail),
        title="Invalid request"
    )
    return response.Message(meta=response.Meta(id=uuid.uuid()), errors=[err])


@app.get("/")
async def get_root():
    return {"msg": "Hello, data science."}
