from importlib.metadata import version

from fastapi import FastAPI

app = FastAPI(
    title="Demo cookiecutter API",
    description="Demo of an API. Created from the StatCan datascience-cookiecutter.",
    version=version("demo_db_api"),
    license_info={
        "name": "MIT",
        "url": "https://github.com/goatsweater/demo-cookiecutter-api/blob/main/LICENSE"
    }
)


@app.get("/")
async def get_root():
    return {"msg": "Hello, data science."}
