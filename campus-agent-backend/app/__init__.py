from fastapi import FastAPI

app = FastAPI()

# Include routes
from .routes import exam

app.include_router(exam.router)

# Additional app configuration can be added here if needed