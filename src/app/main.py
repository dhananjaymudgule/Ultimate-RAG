from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import user, items, upload_router
from src.app.api.routes import upload_router, query  

from src.app.core.config import settings



# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="1.0.0"
)

# CORS Middleware (Allows frontend apps to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# app.include_router(user.router, prefix="/users", tags=["Users"])
# app.include_router(items.router, prefix="/items", tags=["Items"])

# Include the upload router
app.include_router(upload_router, prefix="/files", tags=["File Uploads"])
app.include_router(query.router, prefix="/query", tags=["Query Handling"])  

# Root endpoint
@app.get("/", tags=["Health Check"])
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!", "status": "OK"}


# Run app only if executed directly (not imported)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=True)


