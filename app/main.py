from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="Sample API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World!", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "created_at": datetime.now().isoformat()
    }

@app.post("/users")
async def create_user(user_data: dict):
    return {
        "message": "User created successfully",
        "user_id": 123,
        "data": user_data,
        "created_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)