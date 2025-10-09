from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as api_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="My FastAPI App")

origins = [
    "http://localhost:3000",  # React Dev Server
    "https://file-managment-rag-poc.vercel.app",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
    
)

# include versioned API routes
app.include_router(api_router, prefix="/api/v1")

# ✅ Serve uploads folder as static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI setup  🚀"}
