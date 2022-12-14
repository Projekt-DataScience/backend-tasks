import uvicorn
from fastapi import FastAPI
from routes.tasks import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/api/tasks/docs", redoc_url="/api/tasks/redoc",
              openapi_url="/api/tasks/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)

@app.get("/api/tasks/healthcheck")
def healthcheck():
    return { "Status": "Up" }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)